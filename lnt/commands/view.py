# Mark standard lib imports
import time, datetime, calendar
from decimal import Decimal
import asyncio

# Mark 3rd party lib imports
import click

# Mark Local imports
from lnt.rpc.api import listChannels, getChanInfo, getForwardingHistory, \
        getNodeInfo, getInfo
from lnt.constants import VIEW_CHANNEL_COLUMNS_DEFAULT, VIEW_CHANNEL_COLUMNS_MAP
from lnt.commands.utils.utils import get_1ml_info

loop = asyncio.get_event_loop()

def channel(ctx):
    testnet = ctx.parent.parent.config['LNT'].get('testnet', False)

    # ListChannels RPC call
    channels = listChannels(ctx, active_only=False)

    num_channels_with_peer = {}

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

    # getinfo
    self_info = getInfo(ctx)

    # Per channel chores
    async def get_chan_info_chores(ch_id):
        chan_info = getChanInfo(ctx, chan_id=int(ch_id))

        assumed_peer = chan_info['node1_pub']
        if assumed_peer == self_info['identity_pubkey']:
            assumed_peer = chan_info['node2_pub']

        node_info = getNodeInfo(ctx, assumed_peer)

        channels[ch_id] = { **channels[ch_id], **chan_info, **node_info }

        channels[ch_id]['forward_incoming'] = 0
        channels[ch_id]['forward_outgoing'] = 0
        channels[ch_id]['forwards'] = channels[ch_id]['forward_incoming'] + channels[ch_id]['forward_outgoing']
        channels[ch_id]['local/cap'] = round((Decimal(channels[ch_id]['local_balance'])/ Decimal(channels[ch_id]['capacity']))*100, 2)

        # Count channels by peer
        num_channels_with_peer[channels[ch_id]['remote_pubkey']] = num_channels_with_peer.get(channels[ch_id]['remote_pubkey'], 0) + 1

    async_tasks = []
    for ch_id in list(channels):
       async_tasks.append(loop.create_task(get_chan_info_chores(ch_id)))

    loop.run_until_complete(asyncio.gather(*async_tasks))

    # Sort the things
    if ctx.sort:
        sort_key = VIEW_CHANNEL_COLUMNS_MAP[(ctx.max or ctx.min).upper()]
        sorted_channels = sorted(channels.items(), key=lambda kv: kv[1][sort_key])

    if ctx.max:
        sorted_channels.reverse()

    if ctx.csv:
        header = ",".join(VIEW_CHANNEL_COLUMNS_DEFAULT)
    else:
        header = "\n" + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[0].ljust(21) + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[1].ljust(12) + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[2].ljust(11) + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[3] + "   " + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[4] + "   " + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[5] + "   " + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[6].ljust(19) + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[7].ljust(19) + \
            VIEW_CHANNEL_COLUMNS_DEFAULT[8]

    click.echo(header)

    array = sorted_channels if ctx.sort else channels.keys()
    for value in array:
        ch_id = value[0] if ctx.sort else value
        channel = channels[ch_id]
        rows = []
        format_str = "{},{},{},{}%,{},{},{},{},{}" if ctx.csv else "{} {} {} {}% {} {} {} {} {}"

        if ctx.csv:
            prnt_str = format_str.format(
                            str(ch_id),
                            str(channel['capacity']),
                            str(channel['local_balance']),
                            str(channel['local/cap']),
                            str(channel['forwards']),
                            str(len(channel['pending_htlcs'])),
                            time.strftime('%Y-%m-%d %H:%M', time.gmtime(channel['last_update'])),
                            str(num_channels_with_peer[channel['remote_pubkey']]),
                            str(channel['node'].get('alias', ''))
                            )
        else:
            prnt_str = format_str.format(
                            str(ch_id).ljust(20),
                            str(channel['capacity']).ljust(11),
                            str(channel['local_balance']).ljust(10),
                            str(channel['local/cap']).rjust(8),
                            str(channel['forwards']).ljust(10).rjust(12),
                            str(len(channel['pending_htlcs'])).ljust(15),
                            str(time.strftime('%Y-%m-%d %H:%M', time.gmtime(channel['last_update']))).ljust(18),
                            str(num_channels_with_peer[channel['remote_pubkey']]).ljust(18),
                            str(channel['node'].get('alias', ''))
                            )

        click.echo(prnt_str)
    return

def node(ctx):
    """ Prints a summary of a peer from this node's perspective """
    root_conf = ctx.parent.parent
    testnet = True if root_conf.config['LNT'].get('testnet', 'False') == 'True' else False

    # node data
    nd = {
        'shared_channels': {}
    }

    try:
        node_info = getNodeInfo(ctx, ctx.node_key)
    except Exception as e:
        if 'unable to find node' in str(e.code):
            click.echo('\nUnable to find node in local network graph')
        else:
            # unknown error
            click.echo(e.code)
        return

    nd['alias'] = node_info.node.alias
    nd['total_capacity'] = int(node_info.total_capacity) * 10 ** -8
    nd['num_channels'] = node_info.num_channels

    channels = listChannels(ctx)

    # Assemble all channels we have with node
    for ch_key in channels.keys():
        if channels[ch_key]['remote_pubkey'] == ctx.node_key:
            nd['shared_channels'][ch_key] = channels[ch_key]

    nd['noderank'] = get_1ml_info(testnet, ctx.node_key).get('noderank')

    # Print
    if nd.get('alias', False):
        header = "{} - ( {} )".format(nd['alias'], ctx.node_key)
    else:
        header = "{}".format(ctx.node_key)

    total_capacity = "Total Capacity: {}".format(nd['total_capacity'])

    number_of_channels = "Number of channels: {}".format(nd['num_channels'])

    number_of_shared_channels = "Number of shared channels: {}".format(len(nd['shared_channels']))

    shared_channel_breakdown = None
    if len(nd['shared_channels']) != 0:
        sbc = ''
        for ch_id in nd['shared_channels'].keys():
            channel = nd['shared_channels'][ch_id]

            sbc += '\n' + \
                   '    ChannelID: {}\n'.format(ch_id) + \
                   '    Capacity: {}\n'.format(channel['capacity']) + \
                   '    Local Balance: {}\n'.format(channel['local_balance']) + \
                   '    Remote Balance: {}\n'.format(channel['remote_balance']) + \
                   '    Total Sent: {}\n'.format(channel['total_satoshis_sent']) + \
                   '    Total Recieved: {}'.format(channel['total_satoshis_received']) + \
                   '\n'
        shared_channel_breakdown = sbc

    if nd.get('noderank'):
        ml_header = "1ml link: {}".format(
            "https://1ml.com{}/node/{}".format('/testnet' if testnet else '', ctx.node_key))
    else:
        ml_header = "1ml link: {}".format("Not known to 1ml")

    ml_ranking = None
    if nd.get('noderank'):
        ml_ranking = '    CapacityRank: #{}\n'.format(nd['noderank']['capacity']) + \
                     '    ChannelCountRank: #{}\n'.format(nd['noderank']['channelcount']) + \
                     '    AgeRank: #{}\n'.format(nd['noderank']['age']) + \
                     '    GrowthRank: #{}\n'.format(nd['noderank']['growth'])

    click.echo('\n' +
        header + '\n' +
        len(header)*'-' + '\n' +
        total_capacity + '\n' +
        number_of_channels + '\n' +
        number_of_shared_channels + '\n' +
        (shared_channel_breakdown if shared_channel_breakdown else '') + '\n' +
        ml_header + '\n' +
        ml_ranking if ml_ranking else '' + '\n')

