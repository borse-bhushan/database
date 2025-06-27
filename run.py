"""
# File: run.py
# Description: Main entry point for the application.
"""

from utils.comm_fun import append_path

append_path()


if __name__ == "__main__":

    from utils import environment

    environment.load()
    from py_db import run_server

    # Initialize the database
    run_server()
