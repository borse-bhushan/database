"""
# File: exc/cmn_exc.py
# Description: Common exceptions for the database server.
# This module defines exceptions that are commonly used across the database server.
"""

from . import base, err_msg, codes


class CommonPYDBException(base.BaseExc):
    """
    Generic exception for unknown/unclassified database errors.

    Attributes:
        code (str): Unique error code for tracking.
        message (str): Human-readable error message.
    """

    code = codes.UNKNOWN_EXCEPTION
    message = err_msg.UNKNOWN_EXCEPTION


class DatabaseAlreadyExist(base.BaseExc):
    """
    Raised when attempting to create a database that already exists.

    Args:
        db_name (str): Name of the conflicting database.
    """

    code = codes.DATABASE_ALREADY_EXIST
    message = err_msg.DATABASE_ALREADY_EXIST

    def __init__(self, db_name):
        message = self.message.format(db_name=db_name)
        super().__init__(message, self.code, {"db_name": db_name})


class DatabaseNotExist(base.BaseExc):
    """
    Raised when the specified database does not exist.

    Args:
        db_name (str): Name of the missing database.
    """

    code = codes.DATABASE_DOES_NOT_EXIST
    message = err_msg.DATABASE_DOES_NOT_EXIST

    def __init__(self, db_name):
        message = self.message.format(db_name=db_name)
        super().__init__(message, self.code, {"db_name": db_name})


class TableDoesNotExist(base.BaseExc):
    """
    Raised when the specified table does not exist in the database.

    Args:
        table (str): Name of the missing table.
    """

    code = codes.TABLE_DOES_NOT_EXIST
    message = err_msg.TABLE_DOES_NOT_EXIST

    def __init__(self, table):
        message = self.message.format(table=table)
        super().__init__(message, self.code, {"table": table})


class TableAlreadyExist(base.BaseExc):
    """
    Raised when attempting to create a table that already exists.

    Args:
        table (str): Name of the conflicting table.
    """

    code = codes.TABLE_ALREADY_EXIST
    message = err_msg.TABLE_ALREADY_EXIST

    def __init__(self, table):
        message = self.message.format(table=table)
        super().__init__(message, self.code, {"table": table})


class TableSchemaNotExist(base.BaseExc):
    """
    Raised when the schema for a given table is not found.

    Args:
        table (str): Name of the table whose schema is missing.
    """

    code = codes.TABLE_SCHEMA_NOT_EXIST
    message = err_msg.TABLE_SCHEMA_NOT_EXIST

    def __init__(self, table):
        message = self.message.format(table=table)
        super().__init__(message, self.code, {"table": table})


class DataIsNotValid(base.BaseExc):
    """
    Raised when validation on input data fails.

    Args:
        errors (dict): Details of validation errors.
    """

    code = codes.INVALID_DATA
    message = err_msg.INVALID_DATA

    def __init__(self, errors):
        super().__init__(self.message, self.code, errors)


class UniqueValueFound(base.BaseExc):
    """
    Raised when a unique constraint is violated.

    Args:
        field (str): Name of the unique field.
        value (any): Value that caused the uniqueness conflict.
        ref_data (dict, optional): Additional context.
    """

    code = codes.INVALID_DATA
    message = err_msg.UNIQUE_DATA_ERROR

    def __init__(self, field=None, value=None, ref_data=None):
        super().__init__(
            code=self.code,
            ref_data={"field": field, "value": value},
            message=self.message.format(field=field, value=value),
        )


class AuthenticationException(base.BaseExc):
    """
    Raised when user authentication fails.

    Typically triggered by invalid token or mismatched credentials.
    """

    code = codes.AUTHENTICATION_FAILED
    message = err_msg.AUTHENTICATION_FAILED
