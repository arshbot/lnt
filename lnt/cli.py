import os, sys, click
from .constants import DEFAULT_LNT_DIR

class LntContext(object):

    def __init__(self):
        self.config = {}
        self.verbose = False

    # TODO: Better print implementation
    # def __repr__(self):
    #    return '<LntContext %r>' % self.home

pass_lnt = click.make_pass_decorator(LntContext)


@click.group()
@click.option('--config', metavar='CONFIG', type=click.Path(exists=True,
     file_okay=True, resolve_path=True), default=DEFAULT_LNT_DIR,
         help="Points to a non default config file")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode.')
@click.pass_context
def cli(ctx, config, verbose):
    """ lnt is a command line tool designed to be a better lncli for sysadmins
    and consumers
    """
    # TODO: parse and load config file
    # TODO: if no config file at default, and no conf file specified, create
    # new conf dir
    # 
    ctx.config = config
    ctx.verbose = verbose
