"""
# File: utils/comm_fun.py
# Description: Common utility functions for the application.
"""

from uuid import uuid4
from datetime import datetime


def get_date_time():
    """
    Get the current date and time in a formatted string.
    """
    return datetime.now()


def get_uuid():

    return str(uuid4())
