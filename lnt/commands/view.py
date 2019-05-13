import click
from lnt.cli import pass_context

@click.command("view", short_help="Views an object")
@pass_context
def cli(ctx):
    click.echo("View called!")
    return
