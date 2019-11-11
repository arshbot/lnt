# Mark standard lib imports
from hashlib import sha1
import os, codecs, argparse

# Mark 3rd party lib imports
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc
from PyInquirer import style_from_dict, Token, prompt, Separator
import click

# Mark Local imports
from .utils import utils, rebal
from lnt.graphics import styles

def channel():
    click.echo("Channel created")
    return

def rebalance(ctx):
    stub, macaroon = utils.create_stub(ctx)
    request = ln.ListChannelsRequest(active_only=True)
    response = stub.ListChannels(request, metadata=[('macaroon', macaroon)])

    channels = utils.normalize_channels(response.channels)

    # Prompt the user to select which channels need to be rebalanced
    from_channels = prompt(styles.get_channel_choice_from(channels), style=styles.prompt_style)
    from_channels = [ x.split(",")[1][1:] for x in from_channels['channel_choices_from'] ]

    # Prompt the user to select which channel should the money be rebalanced to
    to_channel = prompt(styles.get_channel_choice_to(channels), style=styles.prompt_style)
    to_channel = to_channel['channel_choices_to'].split(",")[1][1:]

    rebase_image = rebal.construct_rebalance_image(channels, from_channels,
            to_channel, ctx.max)
    rebal.write_rebalance_image(rebase_image, ctx.name)
    return

def invoice():
    click.echo("Invoice created")
    return

def payment():
    click.echo("Payment created")
    return
