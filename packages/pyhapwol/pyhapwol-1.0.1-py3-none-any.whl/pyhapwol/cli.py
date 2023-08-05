""" Command Line Interface for PyHAPWoL """
import click
import logging
from yaml import load
from yaml.loader import SafeLoader
from .bridge import start


@click.command()
@click.option('--config', '-c', default='config.yaml', show_default=True,
              help='Configuration file to use.')
@click.option('--state', '-s', default='homekit.state', show_default=True,
              help='HomeKit State file for persistence.')
@click.option('--debug', '-d', default=False, show_default=False,
              type=click.BOOL, help='Debug messages.')
def run(config, state, debug):
    """Start HomeKit Server with specified configuration and state file."""

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    cfg = {}
    with open(config, 'r') as file:
        cfg = load(file, Loader=SafeLoader)

    start(cfg, state)


if __name__ == "__main__":
    run()
