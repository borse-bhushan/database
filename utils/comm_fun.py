"""
# File: utils/comm_fun.py
# Description: Common utility functions for the application.
"""

import sys
from pathlib import Path


def get_base_dir():
    """Get the base directory of the application."""
    return Path(__file__).resolve().parent.parent


def append_path():
    """
    Append a path to the system path if it is not already present.
    """

    base_dir = get_base_dir()
    if str(base_dir) not in sys.path:
        sys.path.append(str(base_dir))
