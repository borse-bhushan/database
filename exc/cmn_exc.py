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


class DatabaseAlreadyExist(base.BaseExc):
    code = codes.DATABASE_ALREADY_EXIST
    message = err_msg.DATABASE_ALREADY_EXIST

    def __init__(self, db_name, ref_data=None):
        message = self.message.format(db_name=db_name)

        super().__init__(message, self.code, ref_data)
