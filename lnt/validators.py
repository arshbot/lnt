import click
from lnt.constants import VIEW_CHANNEL_COLUMNS_TOTAL

def columns(ctx, param, value):
    """ Validates column parameters for view channels """

    if value and not value.upper() in VIEW_CHANNEL_COLUMNS_TOTAL:
        raise click.BadParameter("Must be a valid view channels column")

    return value