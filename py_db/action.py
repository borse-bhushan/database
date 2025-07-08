"""
Defines the Action class, which encapsulates a parsed client request
into a structured object for the PyDB engine to process.

Includes attributes for action type, query parameters, payload data,
authorization, and table name.
"""

import json


class Action:
    """
    Represents a client request action parsed into a structured object.

    Attributes:
        action (str): The type of database action (e.g., CREATE, SELECT).
        query (dict, optional): Query filters for SELECT, UPDATE, or DELETE actions.
        payload (dict, optional): Data to insert, update, or use in authentication.
        auth (dict, optional): Authentication metadata (e.g., token).
        table (str, optional): Name of the target table.
        user_db_conf (dict): User-specific database configuration (set post-authentication).
    """

    def __init__(self, action, query=None, payload=None, auth=None, table=None):
        """
        Initialize an Action object with details of the requested operation.

        Args:
            action (str): The action to perform (e.g., CREATE, SELECT).
            query (dict, optional): Query conditions.
            payload (dict, optional): Data for creation or update.
            auth (dict, optional): Authentication data.
            table (str, optional): Target table for the action.
        """
        self.query = query
        self.table = table
        self.action = action
        self.payload = payload
        self.auth = auth or {}
        self.user_db_conf = {}

    def __str__(self):
        """
        Generate a string representation of the action for logging/debugging.

        Returns:
            str: A human-readable representation of the Action object.
        """
        act = [self.action]

        if self.table:
            act.append(self.table)

        if self.payload:
            act.append(json.dumps(self.payload))

        if self.query:
            act.append(json.dumps(self.query))

        if self.auth:
            act.append(json.dumps(self.auth))

        return f"Action({', '.join(act)})"
