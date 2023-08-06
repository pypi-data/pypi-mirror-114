import logging

import click
from .commands import init
from . import utils


@click.group()
@click.option("-v", "--verbose", is_flag=True,
              help="Verbose mode for printing debug info")
@utils.pass_config
def main(config, verbose):
    level = logging.FATAL
    if verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    config.root = utils.get_root()


main.add_command(init)

if __name__ == '__main__':
    main()
