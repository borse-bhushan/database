"""
# utils/arg_pars.py
# Description: Argument parser for command line arguments.
"""

import argparse

from . import msg

parser = argparse.ArgumentParser()

parser.add_argument("-e", "--e-file", type=str, help=msg.PATH_TO_CONF_FILE)
