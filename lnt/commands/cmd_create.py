import click
from lnt.cli import pass_context

@click.command("create", short_help="Creates a new object with associated settings")
@pass_context
def cli(ctx):
    click.echo("create called!")
    return
