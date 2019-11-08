# Mark 3rd party lib imports
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc

# Mark local imports
from lnt.commands.utils import utils, rebal

def listChannels(ctx, active_only:bool=False):
    request = ln.ListChannelsRequest(active_only=False)
    response = ctx.stub.ListChannels(request, metadata=[('macaroon', ctx.macaroon)])
    channels = utils.normalize_channels(response.channels)

    return channels

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


