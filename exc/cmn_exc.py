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

    def __init__(self, db_name):
        message = self.message.format(db_name=db_name)

        super().__init__(message, self.code, {"db_name": db_name})


class DatabaseNotExist(base.BaseExc):
    code = codes.DATABASE_DOES_NOT_EXIST
    message = err_msg.DATABASE_DOES_NOT_EXIST

    def __init__(self, db_name):
        message = self.message.format(db_name=db_name)

        super().__init__(message, self.code, {"db_name": db_name})


class TableDoesNotExist(base.BaseExc):
    code = codes.TABLE_DOES_NOT_EXIST
    message = err_msg.TABLE_DOES_NOT_EXIST

    def __init__(self, table):
        message = self.message.format(table=table)

        super().__init__(message, self.code, {"table": table})


class TableAlreadyExist(base.BaseExc):
    code = codes.TABLE_ALREADY_EXIST
    message = err_msg.TABLE_ALREADY_EXIST

    def __init__(self, table):
        message = self.message.format(table=table)

        super().__init__(message, self.code, {"table": table})


class TableSchemaNotExist(base.BaseExc):
    code = codes.TABLE_SCHEMA_NOT_EXIST
    message = err_msg.TABLE_SCHEMA_NOT_EXIST

    def __init__(self, table):
        message = self.message.format(table=table)
        super().__init__(message, self.code, {"table": table})


class AuthenticationException(base.BaseExc):

    code = codes.AUTHENTICATION_FAILED
    message = err_msg.AUTHENTICATION_FAILED
