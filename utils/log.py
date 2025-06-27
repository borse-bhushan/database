"""
# File: utils/log.py
# Description: A simple logging utility for the database server.
# This module provides a function to log messages at different levels.
# It can be used to log debug, info, warning, error, and critical messages.
"""


def log_msg(level, *message):
    """
    Log a message at the specified logging level.
    """
    _msg = " ".join(message)
    print(f"[{level}] ", _msg)
