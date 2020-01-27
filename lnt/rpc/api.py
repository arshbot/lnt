# Mark 3rd party lib imports
import click
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc

# Mark local imports
from lnt.commands.utils import utils, rebal

def listChannels(ctx, active_only:bool=False):
    request = ln.ListChannelsRequest(active_only=False)
    response = ctx.stub.ListChannels(request, metadata=[('macaroon', ctx.macaroon)])
    channels = utils.normalize_channels(response.channels)

    return channels

def getInfo(ctx):
    request = ln.GetInfoRequest()
    response = ctx.stub.GetInfo(request, metadata=[('macaroon', ctx.macaroon)])
    info = utils.normalize_self_info(response)

    return info

def getNodeInfo(ctx, node_key, include_channels:bool=False):
    request = ln.NodeInfoRequest(pub_key=node_key, include_channels=include_channels)
    response = ctx.stub.GetNodeInfo(request, metadata=[('macaroon', ctx.macaroon)])
    node_info = utils.normalize_node_info(response)

    return node_info

def getChanInfo(ctx, chan_id: int):
    request = ln.ChanInfoRequest(chan_id=chan_id)
    response = ctx.stub.GetChanInfo(request, metadata=[('macaroon', ctx.macaroon)])
    chan_info = utils.normalize_get_chan_response(response)

    return chan_info

def getForwardingHistory(ctx, start_time, end_time, num_max_events=10000):
    request = ln.ForwardingHistoryRequest(
        start_time=start_time,
        end_time=end_time,
        num_max_events=num_max_events
    )
    response = ctx.stub.ForwardingHistory(request, metadata=[('macaroon', ctx.macaroon)])

    return tuple(response.forwarding_events)

def closeChannel(ctx, channel_point, streaming:bool, force:bool=False, target_conf:int=None, sat_per_byte:int=None):
    testnet = ctx.parent.parent.config['LNT']['testnet']

    request = ln.CloseChannelRequest(
        channel_point=channel_point,
        force=force,
        target_conf=target_conf,
        sat_per_byte=sat_per_byte,
    )

    for response in ctx.stub.CloseChannel(request, metadata=[('macaroon', ctx.macaroon)]):
        if streaming:
            if response.close_pending:
                tx = response.close_pending.txid[::-1].hex()
                click.echo(
                "Closing Tx Confirming: {}\nView it here: https://blockstream.info{}{}"\
                    .format(tx, '/testnet/' if testnet else '/', tx))
            elif response.chan_close:
                tx = response.chan_close.txid[::-1].hex()
                click.echo(
                "Closing Tx Confirmed: {}\nView it here: https://blockstream.info{}{}"\
                    .format(tx, '/testnet/' if testnet else '/', tx))
                break
        else:
            return response.close_pending.txid[::-1].hex()
