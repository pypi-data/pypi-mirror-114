import logging
from sys import exit

try:
    # IDE support
    logging.debug("Attempting to import cli.cli_entrypoint")
    from cli import cli_entrypoint
except ModuleNotFoundError as e:
    # python -m support
    logging.debug("Caught import error, attempting to import .cli.cli_entrypoint")
    from .cli import cli_entrypoint

if __name__ == '__main__':
    exit(cli_entrypoint())