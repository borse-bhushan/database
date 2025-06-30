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
        if self._action.type == ActionEnum.PING:
            return Response(act_type=ActionEnum.PING, resp_payload={"message": "PONG"})

        if self._action.type == ActionEnum.CREATE:
            return self.create()

        if self._action.type == ActionEnum.SELECT:
            return self.select()

        if self._action.type == ActionEnum.UPDATE:
            return self.update()

        if self._action.type == ActionEnum.DELETE:
            return self.delete()

    def create(self):
        return Response(act_type=ActionEnum.CREATE, resp_payload=self._action.payload)

    def update(self):
        return Response(act_type=ActionEnum.UPDATE, resp_payload=self._action.payload)

    def select(self):
        return Response(act_type=ActionEnum.SELECT, resp_payload=self._action.query)

    def delete(self):
        return Response(act_type=ActionEnum.DELETE, resp_payload=self._action.query)
