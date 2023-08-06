from pathlib import Path

import click

from ..log import logger
from ..merge import update


@click.command()
@click.option(
    '--local',
    '-l',
    nargs=1,
    help='patch donwloaded configuration with content in specified file',
)
@click.option(
    '--output-dir',
    '-o',
    nargs=1,
    help='directory for final config.yaml file, default: ~/.config/clash',
    default='~/.config/clash',
)
@click.argument('url')
@click.help_option('-h')
def merge(url, local, output_dir):
    out = Path(output_dir, 'config.yaml').expanduser().resolve().absolute()
    if local:
        local = Path(local).expanduser().resolve().absolute()
    logger.info('local overrides file: %s', local)
    logger.info('output file: %s', out)
    try:
        update(url, local, out)
    except Exception:
        logger.exception('failed to merge')
    else:
        logger.info('🙌 successfully completed')
