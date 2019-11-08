# Mark standard lib imports
import time, datetime, calendar
from decimal import Decimal

# Mark 3rd party lib imports
import click, grpc

# Mark Local imports
from lnt.rpc.api import listChannels, getChanInfo, getForwardingHistory


def channel(ctx):
    # ListChannels RPC call
    channels = listChannels(ctx, active_only=False)

    num_channels_with_peer = {}

    # Per channel chores
    for ch_id in list(channels):
        chan_info = getChanInfo(ctx, chan_id=int(ch_id))
        channels[ch_id] = { **channels[ch_id], **chan_info }

        # Prep for ForwardHistory call
        channels[ch_id]['forward_incoming'] = 0
        channels[ch_id]['forward_outgoing'] = 0

        # Count channels by peer
        num_channels_with_peer[channels[ch_id]['remote_pubkey']] = num_channels_with_peer.get(channels[ch_id]['remote_pubkey'], 0) + 1

        # Apply rules
        l_b = Decimal(channels[ch_id]['local_balance'])
        r_b = Decimal(channels[ch_id]['remote_balance'])
        cap = Decimal(channels[ch_id]['capacity'])

        if ctx.minlocalbalpercentage and round((l_b/cap)*100, 2) < ctx.minlocalbalpercentage:
            del channels[ch_id]
            continue

        if ctx.maxlocalbalpercentage and round((l_b/cap)*100, 2) > ctx.maxlocalbalpercentage:
            del channels[ch_id]
            continue

        if ctx.minremotebalpercentage and round((r_b/cap)*100, 2) < ctx.minremotebalpercentage:
            del channels[ch_id]
            continue

        if ctx.maxremotebalpercentage and round((r_b/cap)*100, 2) > ctx.maxremotebalpercentage:
            del channels[ch_id]
            continue

        if ctx.minchannelswithpeer and num_channels_with_peer[channels[ch_id]['remote_pubkey']] < ctx.minchannelswithpeer:
            del channels[ch_id]
            continue

        if ctx.maxchannelswithpeer and num_channels_with_peer[channels[ch_id]['remote_pubkey']] > ctx.maxchannelswithpeer:
            del channels[ch_id]
            continue

    fwd_hist_start_time = calendar.timegm((datetime.date.today() - \
        datetime.timedelta(ctx.monthsago*365/12)).timetuple())

    fwd_hist_end_time = calendar.timegm(datetime.date.today().timetuple())

    # ForwardingHistory RPC call
    for fwd_event in getForwardingHistory(ctx, fwd_hist_start_time, fwd_hist_end_time):
        try:
            channels[str(fwd_event.chan_id_in)]['forward_incoming'] += 1
        except KeyError:
            pass
        try:
            channels[str(fwd_event.chan_id_out)]['forward_outgoing'] += 1
        except KeyError:
            pass

    if not ctx.csv:
        header = "\n" + \
            "CHANNEL ID".ljust(21) + \
            "CAPACITY".ljust(11) + \
            "LOCAL_BAL".ljust(11) + \
            "LOCAL/CAP   " + \
            "FORWARDS   " + \
            "PENDING HTLCS   " + \
            "LAST USED".ljust(19) + \
            "CHANNELS W/ PEER"
    else:
        header = ",".join(["CHANNEL ID","CAPACITY","LOCAL_BAL","LOCAL/CAP","FORWARDS","PENDING HTLCS","LAST USED","CHANNELS W/ PEER"])

    click.echo(header)
    for ch_id in channels.keys():
        channel = channels[ch_id]

        rows = []

        format_str = "{} {} {} {}% {} {} {} {}"
        if ctx.csv:
            format_str = "{},{},{},{}%,{},{},{},{}"

        if ctx.csv:
            prnt_str = format_str.format(
                            str(ch_id),
                            str(channel['capacity']),
                            str(channel['local_balance']),
                            str(round((Decimal(channel['local_balance'])/ \
                                Decimal(channel['capacity']))*100, 2)),
                            str(channel['forward_incoming'] + channel['forward_outgoing']),
                            str(len(channel['pending_htlcs'])),
                            time.strftime('%Y-%m-%d %H:%M', time.gmtime(channel['last_update'])),
                            str(num_channels_with_peer[channel['remote_pubkey']])
                            )
        else:
            prnt_str = format_str.format(
                            str(ch_id).ljust(20),
                            str(channel['capacity']).ljust(10),
                            str(channel['local_balance']).ljust(10),
                            str(round((Decimal(channel['local_balance'])/ \
                                Decimal(channel['capacity']))*100, 2)).rjust(8),
                            str(channel['forward_incoming'] + channel['forward_outgoing']).ljust(10).rjust(12),
                            str(len(channel['pending_htlcs'])).ljust(15),
                            str(time.strftime('%Y-%m-%d %H:%M', time.gmtime(channel['last_update']))).ljust(18),
                            str(num_channels_with_peer[channel['remote_pubkey']])
                            )

        click.echo(prnt_str)
    return