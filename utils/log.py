"""
# File: utils/log.py
# Description: A simple logging utility for the database server.
# This module provides a function to log messages at different levels.
# It can be used to log debug, info, warning, error, and critical messages.
"""

import os
import logging

from env import environment

config: dict = environment["LOGGER"]

LOG_LEVEL = config.get("LEVEL") or "DEBUG"

LOG_FORMAT = config.get(
    "FORMAT", "[%(asctime)s] [%(levelname)s] [%(name)s] | %(message)s"
)

DATE_FORMAT = config.get("DATE_FORMAT", "%Y-%m-%d %H:%M:%S")

_loggers = {}  # Cache for named loggers


def log_msg(level, *message):
    """
    Log a message at the specified logging level.
    """
    _msg = " ".join(message)
    get_logger().log(level, _msg)


def get_logger(name: str = config.get("NAME", "py_db_logger").upper()):
    """
    Returns a configured logger instance, based on environment settings.
    """
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    log_to = config.get("LOG_TO", ["console"])

    if "console" in log_to:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    if "file" in log_to:
        log_file_path = config["FILE_PATH"]
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    _loggers[name] = logger
    return logger
