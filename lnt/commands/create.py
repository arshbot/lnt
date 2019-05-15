# Mark standard lib imports
from hashlib import sha1
import os, codecs, argparse

# Mark 3rd party lib imports
import lnt.rpc.rpc_pb2 as ln, lnt.rpc.rpc_pb2_grpc as lnrpc
from PyInquirer import style_from_dict, Token, prompt, Separator
import click, grpc

# Mark Local imports


def create(ctx):
    click.echo("create called!")
    return

def channel():
    click.echo("Channel created")
    return

def rebalance():

    return

def invoice():
    click.echo("Invoice created")
    return

def payment():
    click.echo("Payment created")
    return
