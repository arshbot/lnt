import os, sys, click
from .constants import DEFAULT_DIR_PATH
from .utils import *
from lnt.commands import create as cmd_create

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
@click.option('--config', metavar='CONFIG', type=click.Path(exists=True,
     file_okay=True, resolve_path=True),
         help="Points to a non default config file")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def main(ctx, config, verbose):
    """ lnt is a command line tool designed to be a better lncli for sysadmins
    and consumers
    """
    # TODO: parse and load config file
    # TODO: if no config file at default, and no conf file specified, create
    # new conf dir

    if not config:
        ensure_default_config_exists()
    elif check_config_exists(config):
        # TODO: Parse config
        parsed_config = None
        pass
    else:
        raise Exception("invalid config file provided")

#    ctx.config = parsed_config
    ctx.verbose = verbose


@main.group()
# @click.command("create", short_help="Creates a new object with associated settings")
@click.pass_context
def create(ctx):
    """ Creates a new channel, rebalance, invoice, or payment """
    return

@create.command()
def channel():
    cmd_create.channel()
    return

@create.command()
def rebalance():
    cmd_create.rebalance()
    return

@create.command()
def invoice():
    cmd_create.invoice()
    return

@create.command()
def payment():
    cmd_create.payment()
    return
