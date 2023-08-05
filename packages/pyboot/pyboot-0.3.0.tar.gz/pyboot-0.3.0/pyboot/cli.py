"""Contains the CLI commands."""

import click
import logging
from importlib import metadata
from pathlib import Path
from . import pkgname
from .pyboot import Pyboot, PybootError

logger = logging.getLogger(__name__)


# click entrypoint
@click.group()
@click.option('-v', '--verbose', count=True, help='Set verbosity level.')
@click.version_option(metadata.version(pkgname))
@click.pass_context
def main(ctx, verbose):
    """Scaffold a python3 CLI project."""
    # set log level with format
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    fmt = '[%(levelname)s] %(message)s'

    if verbose == 1:
        logger.setLevel(logging.INFO)
        fmt = '[%(levelname)s] %(message)s'

    elif verbose == 2:
        logger.setLevel(logging.DEBUG)
        fmt = '[%(levelname)s] %(module)s: %(message)s'

    handler = logging.StreamHandler()

    # configure root logger
    formatter = logging.Formatter(fmt=fmt, datefmt='%Y-%m-%dT%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Run the program
    try:
        # load main controller in context
        ctx.obj = Pyboot()

    except PybootError as e:
        click.echo(str(e))


@main.command()
@click.argument('name', nargs=1)
@click.option('-d', '--directory', type=click.Path(), default=Path.cwd(),
              help='Destination directory.')
@click.pass_obj
def cli(pyboot, name, directory):
    """Create project from the cli template."""
    try:
        pyboot.create_project(name.lower(), directory)
    except PybootError as e:
        click.echo(e)
