"""
auth.py

Provides token-based authentication for PyDB operations.

This module includes functionality for generating, validating, and managing
authentication tokens. It also supports excluding specific action types from
authentication requirements.
"""

import secrets

from exc import AuthenticationException

from .action import Action
from .singleton import SingletonMeta


class Authentication(metaclass=SingletonMeta):
    """
    Handles authentication and authorization for PyDB requests using in-memory token mapping.

    Uses a singleton pattern to ensure consistent state throughout the application.

    Attributes:
        _token_user_map (dict): Maps generated tokens to user database configurations.
        _exclude_auth_action_types (list): List of action types that bypass authentication.
    """

    _token_user_map = {}
    _exclude_auth_action_types = []

    def is_authenticated(self, action: Action):
        """
        Check if the provided action is authenticated via a token.

        Args:
            action (Action): The incoming action object containing auth metadata.

        Returns:
            dict: User database configuration if token is valid.

        Raises:
            AuthenticationException: If no valid token is found and the action is not excluded.
        """
        is_action_excluded = self.is_excluded(action.action)

        if is_action_excluded:
            return True

        token = action.auth.get("token")

        if not token or not token in self._token_user_map:
            raise AuthenticationException()

        return self._token_user_map[token]

    def is_excluded(self, action: str):
        """
        Determine if the action type is excluded from authentication.

        Args:
            action (str): Action type string (e.g., "PING", "LOGIN").

        Returns:
            bool: True if authentication is not required for the action.
        """
        if action in self._exclude_auth_action_types:
            return True

        return False

    def add_exclude_action(self, action: str):
        """
        Add an action type to the list of actions that bypass authentication.

        Args:
            action (str): Action name to exclude.

        Returns:
            str: The action name that was added.
        """
        self._exclude_auth_action_types.append(action)
        return action

    def create_token(self, user_db_conf):
        """
        Generate a secure token and associate it with a user configuration.

        Args:
            user_db_conf (dict): The user-specific DB configuration.

        Returns:
            str: A newly generated token (32-character uppercase hex).
        """
        token = secrets.token_hex(16).upper()
        self._token_user_map[token] = user_db_conf

        return token


# Singleton instance of the Authentication class
authentication = Authentication()

