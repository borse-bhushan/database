"""
Defines the Response class used to generate standardized JSON responses
for communication between the database server and client.

Each response includes an action type and an associated payload.
"""

import json


class Response:
    """
    Represents a response object that can be serialized to a standard JSON format.

    Attributes:
        act_type (str): The type of action (e.g., CREATE, SELECT, ERROR).
        resp_payload (Any): The response data or message to include.
    """

    def __init__(self, act_type, resp_payload):
        """
        Initialize the Response object.

        Args:
            act_type (str): The type of action or result.
            resp_payload (Any): The payload or content of the response.
        """
        self.act_type = act_type
        self.resp_payload = resp_payload

    def generate(self):
        """
        Generate the JSON string representation of the response.

        Returns:
            str: JSON-formatted response string.
        """
        return json.dumps({"action_type": self.act_type, "payload": self.resp_payload})
