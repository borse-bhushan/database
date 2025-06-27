"""
# File: server.py
# Description: A simple threaded TCP server that handles requests from clients.
# This server listens for incoming connections and processes requests using a request handler.
# It is designed to handle multiple clients concurrently using threading.
"""

import socketserver


class DBRequestHandler(socketserver.BaseRequestHandler):
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


class ThreadedTCPServer(socketserver.ThreadingTCPServer):
    """
    A threaded TCP server that allows multiple clients to connect concurrently.
    """

    allow_reuse_address = True


if __name__ == "__main__":

    try:
        with ThreadedTCPServer(("127.0.0.1", 9000), DBRequestHandler) as server:
            print("TCP Server running on 127.0.0.1:9000")
            server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped by user.")
