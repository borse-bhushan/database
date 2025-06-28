"""
#file: con_mgt.py
# Description: This module contains the ConnectionHandler class, which is responsible for handling incoming requests to
"""

import socketserver


class ConnectionHandler(socketserver.BaseRequestHandler):
    """Handles incoming requests to the database server.
    This class is responsible for processing client requests and sending responses"""

    def handle(self):
        """Handle the incoming request from the client."""
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            response = f"Echo from server: {data.decode()}"
            self.request.sendall(response.encode())
