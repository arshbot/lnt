import os, sys, click
from configparser import ParsingError, ConfigParser
from lnt.constants import DEFAULT_DIR_PATH
from lnt.utils import *
from lnt.commands import create as cmd_create
from lnt.commands import view as cmd_view


CONTEXT_SETTINGS = dict(auto_envvar_prefix='COMPLEX')

class LntContext(object):

    def __init__(self):
        self.config = {}
        self.verbose = False

    # TODO: Better print implementation
    # def __repr__(self):
    #    return '<LntContext %r>' % self.home

# pass_context = click.make_pass_decorator(LntContext)
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


# @click.command(cls=ComplexCLI, context_settings=CONTEXT_SETTINGS)
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
    # TODO: Set config to config_path in param
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
@click.option('--index', '-i', metavar='INDEX', help="Channel index to output")
@click.pass_context
def channel(ctx, index):
    ctx.index = index
    cmd_view.channel(ctx)
    return