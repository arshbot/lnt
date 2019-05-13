import click
from lnt.cli import main

@main.group()
# @click.command("create", short_help="Creates a new object with associated settings")
@click.pass_context
def create(ctx):
    click.echo("create called!")
    return

@create.command()
def channel():
    click.echo("Channel created")
    return

@create.command()
def rebalance():
    click.echo("Rebalance created")
    return

@create.command()
def invoice():
    click.echo("Invoice created")
    return

@create.command()
def payment():
    click.echo("Payment created")
    return
