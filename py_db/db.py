from utils import log_msg, logging

from .action import Action
from .storage import Storage
from .response import Response
from .constants import ActionEnum


class PyDB:

    def __init__(self, action: Action):

        self._action = action
        self._storage_engine = Storage()

        log_msg(logging.DEBUG, str(self._action))

    def run(self):
        if self._action.action == ActionEnum.PING:
            return Response(act_type=ActionEnum.PING, resp_payload={"message": "PONG"})

        match self._action.action:

            case ActionEnum.CREATE:
                return self.create()

            case ActionEnum.SELECT:
                return self.select()

            case ActionEnum.UPDATE:
                return self.update()

            case ActionEnum.DELETE:
                return self.delete()

            case ActionEnum.CREATE_DATABASE:
                return self.create_database()

    def create(self):
        return Response(
            act_type=ActionEnum.CREATE,
            resp_payload=self._action.payload,
        )

    def update(self):
        return Response(
            act_type=ActionEnum.UPDATE,
            resp_payload=self._action.payload,
        )

    def select(self):
        return Response(
            act_type=ActionEnum.SELECT,
            resp_payload=self._action.query,
        )

    def delete(self):
        return Response(
            act_type=ActionEnum.DELETE,
            resp_payload=self._action.query,
        )

    def create_database(self):
        self._storage_engine.create_database(self._action.payload)

        return Response(
            act_type=ActionEnum.CREATE_DATABASE,
            resp_payload=self._action.payload,
        )
