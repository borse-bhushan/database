"""
init_db.py

Initializes and preloads databases using the provided configuration list.

This module is typically used to bootstrap a fresh PyDB instance
with one or more databases during startup or installation.
"""

from py_db.storage import Storage


def load_ini_data_in_database(database_conf: list):
    """
    Create databases based on the provided configuration list.

    Args:
        database_conf (list): A list of dictionaries, each containing a database's configuration.
                              Each config should at minimum include the "NAME" field.

    Example:
        load_ini_data_in_database([
            {"NAME": "inventory", "USER": "admin", "PASSWORD": "admin@123"},
            {"NAME": "logs", "USER": "root", "PASSWORD": "root123"},
        ])
    """
    storage_engine = Storage()
    for db_conf in database_conf:
        storage_engine.create_database(db_conf)
