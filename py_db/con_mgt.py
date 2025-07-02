"""
#file: con_mgt.py
# Description: This module contains the ConnectionHandler class,
# which is responsible for handling incoming requests to
"""

import json
import socketserver

from exc import err_msg, codes, base

from .db import PyDB
from .action import Action
from .response import Response
from .auth import authentication
from .constants import ActionEnum

from utils import log_msg, logging


class ConnectionHandler(socketserver.BaseRequestHandler):
    """Handles incoming requests to the database server.
    This class is responsible for processing client requests and sending responses"""

    def handle(self):
        """
        Receives data from the socket, handling the custom header format.
        The header is expected to be in the format:
        QUERY_LENGTH: <length>\r\n\r\n
        where <length> is the length of the query data that follows.
        The body will be read until the specified length is reached.
        If the header is not fully received, it will keep reading until it is.
        If the body is not fully received, it will keep reading until the specified
        length is reached.
        """

        buffer = b""
        # Read initial chunk
        chunk = self.request.recv(1024)
        if not chunk:
            log_msg(logging.DEBUG, f"CLOSING CONNECTION {self.client_address[0]}:{self.client_address[1]}"),
            return

        buffer += chunk

        # Find the header delimiter
        delimiter = b"\r\n\r\n"
        header_end = buffer.find(delimiter)
        if header_end == -1:
            # Header not fully received yet, keep reading until we get it
            while header_end == -1:
                chunk = self.request.recv(1024)
                if not chunk:
                    return
                buffer += chunk
                header_end = buffer.find(delimiter)

        # Extract header and body
        header = buffer[:header_end].decode()
        body = buffer[header_end + len(delimiter) :]

        # Parse query length from header
        query_length = None
        for line in header.splitlines():
            if line.startswith("QUERY_LENGTH"):
                try:
                    query_length = int(line.split(":")[1].strip())
                except (IndexError, ValueError):
                    self.send(
                        Response(
                            act_type=ActionEnum.ERROR,
                            resp_payload={
                                "message": err_msg.QUERY_LENGTH,
                                "code": codes.QUERY_LENGTH,
                            },
                        ).generate()
                    )
                    return
                break

        if query_length is None:
            self.send(
                Response(
                    act_type=ActionEnum.ERROR,
                    resp_payload={
                        "message": err_msg.MISSING_QUERY_LENGTH,
                        "code": codes.QUERY_LENGTH,
                    },
                ).generate()
            )
            return

        # Read the rest of the body if not fully received
        while len(body) < query_length:
            chunk = self.request.recv(1024)
            if not chunk:
                break
            body += chunk

        # Now body contains the full data of length query_length
        query_data = body[:query_length]

        # Example: echo back the received data length
        query_data = query_data.decode()
        self.send_action_to_db(query_data)

    def send(self, data: str):
        """Send data to the client with QUERY_LENGTH header and delimiter."""
        header = f"QUERY_LENGTH: {len(data)}\r\n\r\n"
        self.request.sendall((header + data).encode())

    def handle_exc(self, exc: base.BaseExc):

        self.send(
            Response(
                act_type=ActionEnum.ERROR,
                resp_payload={
                    "code": exc.code,
                    "message": exc.message,
                    "ref_data": exc.ref_data,
                },
            ).generate()
        )

        self.handle()

    def send_action_to_db(self, action):

        try:

            action = Action(**json.loads(action))

            user_db_conf = authentication.is_authenticated(action)
            action.user_db_conf = user_db_conf

            py_db = PyDB(action=action)

            response: Response = py_db.run()

            self.send(response.generate())

            self.handle()

        except base.BaseExc as exc:
            self.handle_exc(exc)
