"""
# File: exc/base.py
# Description: Base exception class for the database server.
# This module defines a base exception class that can be used
# to handle errors in the database server.
# It allows for custom error messages and codes to be set when raising exceptions.
"""

from . import codes, err_msg


class BaseExc(Exception):
    """Base class for all exceptions in this module."""

    code = codes.UNKNOWN_EXCEPTION
    message = err_msg.UNKNOWN_EXCEPTION

    def __init__(self, message=None, code=None, ref_data=None):
        """
        Initialize the exception with an optional message.
        If no message is provided, use the default message.
        """
        self.code = code
        self.message = message
        self.ref_data = ref_data

        super().__init__(self.message)
