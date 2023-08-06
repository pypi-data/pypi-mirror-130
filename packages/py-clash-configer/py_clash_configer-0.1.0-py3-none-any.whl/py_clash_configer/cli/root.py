import click

from ..log import logger
from .context import CliContext

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(
    'py-clash-configer',
    context_settings=CONTEXT_SETTINGS,
)
@click.pass_context
@click.option('--debug/--no-debug')
def root(ctx: click.Context, debug: bool):
    obj = ctx.ensure_object(CliContext)
    obj.debug = debug

    if obj.debug:
        logger.setLevel('DEBUG')

    logger.debug(ctx.obj)
