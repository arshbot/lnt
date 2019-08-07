# Mark standard lib imports
import time, datetime, calendar
from decimal import Decimal

# Mark 3rd party lib imports
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc
import click, grpc

# Mark Local imports
from .utils import utils, rebal

from ptpdb import set_trace

def channel(ctx):
    stub, macaroon = utils.create_stub(ctx)

    # ListChannels RPC call
    request = ln.ListChannelsRequest(active_only=True)
    response = stub.ListChannels(request, metadata=[('macaroon', macaroon)])
    channels = utils.normalize_channels(response.channels)

    monthsago = ctx.monthsago
    if 'DefaultMonthsAgo' in ctx.find_root().config['LNT'].keys():
        monthsago = ctx.find_root().config['LNT']['DefaultMonthsAgo']

    # GetChanInfo RPC call ( per channel )
    for ch_id in channels.keys():
        request = ln.ChanInfoRequest(chan_id=int(ch_id))
        response = stub.GetChanInfo(request, metadata=[('macaroon', macaroon)])
        chan_info = utils.normalize_get_chan_response(response)
        channels[ch_id] = { **channels[ch_id], **chan_info }
        
        # Prep for ForwardHistory call
        channels[ch_id]['forward_incoming'] = 0
        channels[ch_id]['forward_outgoing'] = 0


    # ForwardingHistory RPC call
    fwd_hist_start_time = calendar.timegm((datetime.date.today() - \
        datetime.timedelta(monthsago*365/12)).timetuple())
    
    fwd_hist_end_time = calendar.timegm(datetime.date.today().timetuple())
    
    request = ln.ForwardingHistoryRequest(
        start_time=fwd_hist_start_time,
        end_time=fwd_hist_end_time,
    )
    response = stub.ForwardingHistory(request, metadata=[('macaroon', macaroon)])

    for fwd_event in tuple(response.forwarding_events):
        try:
            channels[fwd_event.chan_id_in]['forward_incoming'] += 1
            channels[fwd_event.chan_id_out]['forward_outgoing'] += 1
            click.echo("SUCCESS")
        except KeyError:
            continue

    set_trace()

    click.echo("\n" + "CHANNEL ID".ljust(21) + "CAPACITY".ljust(11) + "LOCAL_BAL".ljust(11) + \
        "LOCAL/CAP" + "   UPDATE NUM" + "   PENDING HTLCS" + "   LAST USED")
    for ch_id in channels.keys():
        channel = channels[ch_id]
        click.echo("{} {} {} {}% {} {} {}".format(
                                str(ch_id).ljust(20),
                                str(channel['capacity']).ljust(10),
                                str(channel['local_balance']).ljust(10),
                                str(round((Decimal(channel['local_balance'])/ \
                                    Decimal(channel['capacity']))*100, 2)).rjust(8),
                                str(channel['num_updates']).rjust(12),
                                str(len(channel['pending_htlcs'])).rjust(3).ljust(17),
                                time.strftime('%Y-%m-%d %H:%M', time.gmtime(channel['last_update'])),
                                ))
    return