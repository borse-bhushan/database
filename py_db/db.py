from utils import log_msg, logging
from exc import AuthenticationException, CommonPYDBException, err_msg, codes

from .action import Action
from .storage import Storage
from .response import Response
from .constants import ActionEnum

from .auth import authentication


class PyDB:

    def __init__(self, action: Action):

        self._action = action
        self._storage_engine = Storage()

        log_msg(logging.DEBUG, str(self._action))

    def run(self):

        if self._action.action == ActionEnum.PING:
            return Response(act_type=ActionEnum.PING, resp_payload={"message": "PONG"})

        match self._action.action:

            case ActionEnum.CREATE_TABLE:
                return self.create_table()

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

            case ActionEnum.LOGIN:
                return self.login()

            case ActionEnum.DROP_TABLE:
                return self.drop_table()

        return Response(
            ActionEnum.ERROR,
            resp_payload={
                "message": f"'{self._action.action}' invalid action.",
            },
        )

    def create_table(self):

        resp_data = self._storage_engine.create_table(
            table=self._action.table,
            schema_def=self._action.payload,
            database=self._action.user_db_conf["NAME"],
        )
        return Response(
            resp_payload=resp_data,
            act_type=ActionEnum.CREATE_TABLE,
        )

    def create(self):

        if not self._action.table:
            raise CommonPYDBException(
                code=codes.TABLE_NOT_PROVIDED,
                message=err_msg.TABLE_NOT_PROVIDED.format(action=self._action.action),
            )

        data = self._storage_engine.insert_data(
            table=self._action.table,
            data=self._action.payload,
            database=self._action.user_db_conf["NAME"],
        )

        resp_data = {"data": data, "table": self._action.table}

        return Response(
            resp_payload=resp_data,
            act_type=ActionEnum.CREATE,
        )

    def update(self):

        updated_rows = self._storage_engine.update(
            table=self._action.table,
            query=self._action.query,
            update_data=self._action.payload,
            database=self._action.user_db_conf["NAME"],
        )

        return Response(
            act_type=ActionEnum.UPDATE,
            resp_payload={"count": updated_rows},
        )

    def select(self):

        results = self._storage_engine.read(
            table=self._action.table,
            query=self._action.query,
            database=self._action.user_db_conf["NAME"],
        )

        return Response(
            act_type=ActionEnum.SELECT,
            resp_payload=results,
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

    def drop_table(self):
        self._storage_engine.drop_table(
            table=self._action.table,
            database=self._action.user_db_conf["NAME"],
        )
        return Response(
            act_type=ActionEnum.DROP_TABLE,
            resp_payload={},
        )

    def login(self):

        database_conf = self._storage_engine.read_db_conf(
            self._action.payload["database"]
        )

        if not database_conf["USER"] == self._action.payload["user"]:
            raise AuthenticationException()

        if not database_conf["PASSWORD"] == self._action.payload["password"]:
            raise AuthenticationException()

        return Response(
            act_type=ActionEnum.LOGIN,
            resp_payload={
                "token": authentication.create_token(database_conf),
            },
        )
