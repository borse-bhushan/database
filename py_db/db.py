from .action import Action
from .response import Response
from .constants import ActionEnum


class PyDB:

    def __init__(self, action: Action):

        self._action = action

    def run(self):
        if self._action.type == ActionEnum.PING:
            return Response(act_type=ActionEnum.PING, resp_payload={"message": "PONG"})
