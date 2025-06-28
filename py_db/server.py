"""
# File: server.py
# Description: A simple threaded TCP server that handles requests from clients.
# This server listens for incoming connections and processes requests using a request handler.
# It is designed to handle multiple clients concurrently using threading.
"""

import socketserver

from env import environment
from utils import log_msg, logging

from .con_mgt import ConnectionHandler


class ThreadedTCPServer(socketserver.ThreadingTCPServer):
    """
    A threaded TCP server that allows multiple clients to connect concurrently.
    """

    allow_reuse_address = True


def run_server():
    """
    Run the threaded TCP server.
    This function initializes the server and starts listening for incoming connections.
    It will run until interrupted by a keyboard signal (Ctrl+C).
    It logs the server's status and handles shutdown gracefully.
    """

    try:
        host = environment["HOST"]
        port = environment["PORT"]

        with ThreadedTCPServer((host, port), ConnectionHandler) as server:
            log_msg(logging.DEBUG, f"PYDB RUNNING ON: [{host}:{port}]")
            server.serve_forever()

    except KeyboardInterrupt:
        log_msg(logging.DEBUG, "SERVER SHUTTING DOWN")
