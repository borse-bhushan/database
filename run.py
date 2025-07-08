"""
# Description: Main entry point for the application.
"""

from env import environment

environment.setup()

if __name__ == "__main__":

    from py_db import run_server

    # Initialize the database
    run_server()
