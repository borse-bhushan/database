import secrets

from exc import AuthenticationException

from .action import Action
from .singleton import SingletonMeta


class Authentication(metaclass=SingletonMeta):

    _token_user_map = {}
    _exclude_auth_action_types = []

    def is_authenticated(self, action: Action):

        is_action_excluded = self.is_excluded(action.action)

        if is_action_excluded:
            return True

        token = action.auth.get("token")

        if not token or not token in self._token_user_map:
            raise AuthenticationException()

        return self._token_user_map[token]

    def is_excluded(self, action: str):

        if action in self._exclude_auth_action_types:
            return True

        return False

    def add_exclude_action(self, action: str):
        self._exclude_auth_action_types.append(action)
        return action

    def create_token(self, user_db_conf):

        token = secrets.token_hex(16).upper()
        self._token_user_map[token] = user_db_conf

        return token


authentication = Authentication()
