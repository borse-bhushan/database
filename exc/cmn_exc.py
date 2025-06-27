"""
# File: exc/cmn_exc.py
# Description: Common exceptions for the database server.
# This module defines exceptions that are commonly used across the database server.
"""

from . import base, err_msg, codes


class CommonPYDBException(base.BaseExc):
    """Exception raised when the configuration file is not found."""

    code = codes.UNKNOWN_EXCEPTION
    message = err_msg.UNKNOWN_EXCEPTION
