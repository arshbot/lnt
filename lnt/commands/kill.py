# Mark 3rd party imports
import click

# Mark Local imports
import lnt.rpc.rpc_pb2 as ln
from lnt.rpc.api import getChanInfo, closeChannel
from .utils import utils


def channel(ctx):
    testnet = ctx.parent.parent.config['LNT'].getboolean('testnet', False)
    chan_info = getChanInfo(ctx, ctx.channel_id)
    funding_txid, output_index = chan_info['chan_point'].split(':')

    channel_point = ln.ChannelPoint(
        funding_txid_str=funding_txid,
        output_index=int(output_index)
    )

    closing_tx = None
    try:
        closing_tx = closeChannel(ctx, channel_point, streaming=ctx.streaming, force=ctx.force, target_conf=ctx.target_conf, sat_per_byte=ctx.sat_per_byte)
    except Exception as error:
        if "unable to gracefully close channel while peer is offline" in str(error):
            click.echo("Error: Peer is offline, rerun with -f")
        elif "channel is already in the process of being force closed" in str(error):
            click.echo("Warning: Channel is already in the process of being force closed")
        elif "force closing a channel uses a pre-defined fee" in str(error):
            click.echo("Force closing uses a pre-defined fee. Closing of channel abandoned")
        else:
            click.echo("Unhandled Error: " + str(error))
        return

    if not ctx.streaming:
        click.echo(
        "Closing Tx Confirming: {}\nView it here: https://blockstream.info{}{}"\
            .format(closing_tx, '/testnet/' if testnet else '/', closing_tx))

    return


