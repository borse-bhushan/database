"""
# File: exc/err_msg.py
# Description: Error messages for the database server.
"""

QUERY_LENGTH = "Invalid Query Length."
UNKNOWN_EXCEPTION = "Unknown Exception."
MISSING_QUERY_LENGTH = "Missing Query Length."
AUTHENTICATION_FAILED = "Authentication Failed."
UNIQUE_DATA_ERROR = "{field}:{value} is already exist."
TABLE_NOT_PROVIDED = "Table is not provided for {action}"
DATABASE_ALREADY_EXIST = "({db_name}) Database Already Exist."
TABLE_ALREADY_EXIST = "({table}) Table Already Exist."
INVALID_DATA = "Invalid data."
TABLE_SCHEMA_NOT_EXIST = "({table}) Schema does not exist."
DATABASE_DOES_NOT_EXIST = "({db_name}) Database does not exist"
TABLE_DOES_NOT_EXIST = "({table}) Table does not exist"
CONFIG_FILE_NOT_FOUND = "Configuration file not found ({file_path})."
INVALID_CONFIG_JSON_FILE = (
    "Invalid JSON format in the configuration file ({file_path})."
)
