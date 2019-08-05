# Mark standard lib imports
import time
from decimal import Decimal

# Mark 3rd party lib imports
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc
import click, grpc

# Mark Local imports
from .utils import utils, rebal

def channel(ctx):
    stub, macaroon = utils.create_stub(ctx)
    request = ln.ListChannelsRequest(active_only=True)
    response = stub.ListChannels(request, metadata=[('macaroon', macaroon)])

    channels = utils.normalize_channels(response.channels)

    for ch_id in channels.keys():
        request = ln.ChanInfoRequest(chan_id=int(ch_id))
        response = stub.GetChanInfo(request, metadata=[('macaroon', macaroon)])
        chan_info = utils.normalize_get_chan_response(response)
        channels[ch_id] = { **channels[ch_id], **chan_info }

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