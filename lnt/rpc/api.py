# Mark 3rd party lib imports
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc

# Mark local imports
from .utils import utils, rebal

STUB, MACAROON = utils.create_stub(ctx)

def listChannels(active_only:bool=False):
    request = ln.ListChannelsRequest(active_only=False)
    response = STUB.ListChannels(request, metadata=[('macaroon', MACAROON)])
    channels = utils.normalize_channels(response.channels)

    return channels

def getChanInfo(chan_id: int):
    request = ln.ChanInfoRequest(chan_id=chan_id)
    response = STUB.GetChanInfo(request, metadata=[('macaroon', MACAROON)])
    chan_info = utils.normalize_get_chan_response(response)

    return chan_info

def getForwardingHistory(start_time, end_time, num_max_events=10000):
    request = ln.ForwardingHistoryRequest(
        start_time=start_time,
        end_time=end_time,
        num_max_events=num_max_events
    )
    response = stub.ForwardingHistory(request, metadata=[('macaroon', macaroon)])

    return tuple(response.forwarding_events)


