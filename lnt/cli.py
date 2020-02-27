import os, sys, click
from decimal import Decimal
from configparser import ParsingError, ConfigParser
from lnt.constants import DEFAULT_DIR_PATH, DEFAULT_MONTHS_AGO
from lnt.utils import *
from lnt.commands import create as cmd_create
from lnt.commands import view as cmd_view
from lnt.commands import kill as cmd_kill
from lnt.commands.utils import utils
from lnt import validators


CONTEXT_SETTINGS = dict(auto_envvar_prefix='COMPLEX')

class LntContext(object):

    def __init__(self):
        self.config = {}
        self.verbose = False

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))

class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('lnt.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            click.echo("Failed" + name)
            return
        return mod.cli


@click.group(invoke_without_command=True)
@click.option('--config', metavar='CONFIG_PATH', type=click.Path(exists=True,
     file_okay=True, resolve_path=True, readable=True),
         help='Points to a non default config file.')
@click.option('--verbose', is_flag=True, help='Enables verbose mode.')
@click.option('--version', is_flag=True, help='Prints the version.')
@click.pass_context
def main(ctx, config, verbose, version):
    """ lnt is a command line tool designed to be a better lncli for sysadmins
    and consumers
    """

    if version:
        import pkg_resources  # part of setuptools
        click.echo(pkg_resources.require("lnt")[0].version)

    # TODO: Allow for custom lnt dir
    config_path = config

    if not config_path:

        # Default lnt dir is in constants.py
        if not check_lnt_folder_exists():
            create_lnt_folder()

        # Checks if the default config is available
        if not check_config_exists():
            create_config()

        config_path = const.DEFAULT_CONF_PATH

    config = ConfigParser()

    # Config validation
    try:
        config.read(config_path)
        config, passed = validate_config(config)

        if not passed:
            raise Exception

    except Exception:
        raise Exception("Invalid config file provided")

    ctx.config = config
    ctx.verbose = verbose

# Disabling because not implemented
# 
# @main.group()
# @click.pass_context
# def create(ctx):
#     """ Creates a new channel, rebalance, invoice, or payment """
#     return
# 
# @create.command()
# def channel():
#     cmd_create.channel()
#     return
# 
# 
# @create.command()
# @click.option('--max', '-m', is_flag=True, help="Rebalance maximum amount from channels")
# @click.option('--name', '-n', metavar='NAME', help="Name a rebalance image")
# @click.pass_context
# def rebalance(ctx, max, name):
#     ctx.max = max
#     ctx.name = name
#     cmd_create.rebalance(ctx)
#     return
# 
# @create.command()
# def invoice():
#     cmd_create.invoice()
#     return
# 
# @create.command()
# def payment():
#     cmd_create.payment()
#     return

@main.group()
@click.pass_context
def view(ctx):
    """ View channels, rebalances, invoices, or payments """
    return

@view.command()
# TODO: Add channel row indexing
# @click.option('--index', '-i', metavar='INDEX', help="Channel index to output")
@click.option('--csv', is_flag=True, help="Channel index to output")
@click.option('--monthsago', '-m', metavar='MONTHS_AGO',
    help="Shows events up to x months ago")
@click.option('--max', metavar='COLUMN', help="Sorts COLUMN by max", callback=validators.columns)
@click.option('--min', metavar='COLUMN', help="Sorts COLUMN by min", callback=validators.columns)
@click.pass_context
def channel(ctx, csv, monthsago, max, min):
    """ Payment channel """
    ctx.sort = None
    ctx.csv = csv
    ctx.max = max
    ctx.min = min

    if ctx.max or ctx.min:
        if ctx.min and ctx.min.lower() in ['num_channels_with_peer', 'last_update', 'pending_htlcs',\
             'channel_id', 'alias']:
            raise click.BadParameter('Sorting for these COLUMNS are not implemented yet.')
        if ctx.max and ctx.max.lower() in ['num_channels_with_peer', 'last_update', 'pending_htlcs',\
             'channel_id', 'alias']:
            raise click.BadParameter('Sorting for these COLUMNS are not implemented yet.')

        ctx.sort = True

    if ctx.max and ctx.min:
        raise click.BadParameter("max and min options are mutually exclusive.")

    ctx.stub, ctx.macaroon = utils.create_stub(ctx)

    if monthsago:
        ctx.monthsago = monthsago
    elif 'MonthsAgo' in ctx.find_root().config['LNT'].keys():
        ctx.monthsago = ctx.find_root().config['LNT']['MonthsAgo']
    else:
        ctx.monthsago = DEFAULT_MONTHS_AGO
    ctx.monthsago = int(ctx.monthsago)

    cmd_view.channel(ctx)
    return

@view.command()
@click.argument('node_key', nargs=1)
@click.pass_context
def node(ctx, node_key):
    """ Lnd node """
    ctx.node_key = node_key
    ctx.stub, ctx.macaroon = utils.create_stub(ctx)

    cmd_view.node(ctx)

@main.group()
@click.pass_context
def kill(ctx):
    """ Kill channels """
    return

@kill.command()
@click.option('--id', metavar='CHANNEL_ID', help="Close by channel id", type=int)
@click.option('-f', is_flag=True, help="Closes a channel uncooperatively ( force close )")
@click.option('--streaming', '-s', is_flag=True, help="Listens for updates on the closed channel")
@click.option('--target_conf', metavar='NUM_BLOCKS', help="Target confirmation blocks", type=int)
@click.option('--sat_per_byte', metavar='SATS', help="Feerate in satoshis per byte for closing tx", type=Decimal)
@click.pass_context
def channel(ctx, id, f, streaming, target_conf, sat_per_byte):
    ctx.channel_id = id
    ctx.force = f
    ctx.streaming = streaming
    ctx.target_conf = target_conf
    ctx.sat_per_byte = sat_per_byte
    ctx.stub, ctx.macaroon = utils.create_stub(ctx)

    cmd_kill.channel(ctx)

