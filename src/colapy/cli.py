import click
import typing as tp
import os

from . import RunManager
from ._cli_lib import cli


@cli.command()
@click.option('--config', required=True, help='Calculation description config path')
@click.option('-l', '--library', multiple=True, help='Path to library')
@click.option('-n', '--steps', type=int, default=1, help='Steps to run the simulation')
def run(config: str, library: tp.List[str], steps: int):
    manager = RunManager()
    for lib in library:
        manager.load_library(lib, os.path.expanduser('~/.local/lib'))
    manager.load_config(os.path.expanduser(config))
    manager.run(steps)


def main():
    cli()
