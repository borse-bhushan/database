"""
# Description: Argument parser for command line arguments.
"""

import argparse

PATH_TO_CONF_FILE = "Path to env.json file"
LOAD_INITIAL_DATA = "Load initial data flag"


def get_parser():
    """
    Returns an argument parser for command line arguments.

    Returns:
        argparse.ArgumentParser: The argument parser instance.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--e-file", type=str, help=PATH_TO_CONF_FILE)

    parser.add_argument(
        "-lid", "--load-initial-data", action="store_true", help=LOAD_INITIAL_DATA
    )

    return parser.parse_args()


args = get_parser()
