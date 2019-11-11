import os, sys, click
from decimal import Decimal
from configparser import ParsingError, ConfigParser
from lnt.constants import DEFAULT_DIR_PATH, DEFAULT_MONTHS_AGO
from lnt.utils import *
from lnt.commands import create as cmd_create
from lnt.commands import view as cmd_view
from lnt.commands import kill as cmd_kill
from lnt.commands.utils import utils


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


@click.group()
@click.option('--config', metavar='CONFIG_PATH', type=click.Path(exists=True,
     file_okay=True, resolve_path=True, readable=True),
         help="Points to a non default config file")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def main(ctx, config, verbose):
    """ lnt is a command line tool designed to be a better lncli for sysadmins
    and consumers
    """
    # TODO: Allow for custom lnt dir
    config_path = config


    if not config_path:

        # Default lnt dir is in constants.py
        if not check_lnt_folder_exists():
            create_lnt_folder()

        # Checks if the default config is available
        if not check_config_exists():
            create_config()
            raise click.FileError(filename="config", hint="Error: please configure config at "+const.DEFAULT_CONF_PATH)

        config_path = const.DEFAULT_CONF_PATH

    config = ConfigParser()

    # Config validation
    try:
        config.read(config_path)
        validate_config(config)
    except ParsingError:
        raise Exception("Invalid config file provided")

    ctx.config = config
    ctx.verbose = verbose


@main.group()
@click.pass_context
def create(ctx):
    """ Creates a new channel, rebalance, invoice, or payment """
    return

@create.command()
def channel():
    cmd_create.channel()
    return

@create.command()
@click.option('--max', '-m', is_flag=True, help="Rebalance maximum amount from channels")
@click.option('--name', '-n', metavar='NAME', help="Name a rebalance image")
@click.pass_context
def rebalance(ctx, max, name):
    ctx.max = max
    ctx.name = name
    cmd_create.rebalance(ctx)
    return

@create.command()
def invoice():
    cmd_create.invoice()
    return

@create.command()
def payment():
    cmd_create.payment()
    return

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
@click.option('--minlocalbalpercentage', '-mil', metavar='MIN_LOCAL_BAL_PERCENTAGE',
    help="Shows channels whose local balance is at least x percentage", type=int)
@click.option('--maxlocalbalpercentage', '-mal', metavar='MAX_LOCAL_BAL_PERCENTAGE',
    help="Shows channels whose local balance is at most x percentage", type=int)
@click.option('--minremotebalpercentage', '-mir', metavar='MIN_REMOTE_BAL_PERCENTAGE',
    help="Shows channels whose remote balance is at least x percentage", type=int)
@click.option('--maxremotebalpercentage', '-mar', metavar='MAX_REMOTE_BAL_PERCENTAGE',
    help="Shows channels whose remote balance is at most x percentage", type=int)
@click.option('--minchannelswithpeer', '-mip', metavar='MIN_CHANNELS_WITH_PEER',
    help="Shows channels who have at least x total channels with peer", type=int)
@click.option('--maxchannelswithpeer', '-map', metavar='MAX_CHANNELS_WITH_PEER',
    help="Shows channels who have at most x total channels with peer", type=int)
@click.pass_context
def channel(ctx, csv, monthsago, minlocalbalpercentage, maxlocalbalpercentage,
        minremotebalpercentage, maxremotebalpercentage, minchannelswithpeer,
        maxchannelswithpeer):
    ctx.csv = csv
    ctx.minlocalbalpercentage = minlocalbalpercentage
    ctx.maxlocalbalpercentage = maxlocalbalpercentage
    ctx.minremotebalpercentage = minremotebalpercentage
    ctx.maxremotebalpercentage = maxremotebalpercentage
    ctx.minchannelswithpeer = minchannelswithpeer
    ctx.maxchannelswithpeer = maxchannelswithpeer

    ctx.stub, ctx.macaroon = utils.create_stub(ctx)

    if monthsago:
        ctx.monthsago = monthsago
    elif 'MonthsAgo' in ctx.find_root().config['LNT'].keys():
        ctx.monthsago = ctx.find_root().config['LNT']['MonthsAgo']
    else:
        ctx.monthsago = DEFAULT_MONTHS_AGO
    ctx.monthsago = int(ctx.monthsago)

    # if minlocalbalpercentage and maxlocalbalpercentage:
    #     if minlocalbalpercentage > maxlocalbalpercentage:
    #         raise click.BadParameter(message="minlocalbalpercentage cannot be greater than maxlocalbalpercentage")

    cmd_view.channel(ctx)
    return

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

