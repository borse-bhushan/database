"""
pydb.py

Defines the PyDB class, which acts as the core controller for executing
database operations based on a parsed `Action` object.

This class delegates actual storage interactions to the `Storage` engine
and handles supported actions such as creating tables, inserting records,
running queries, and authenticating users.

Responses are returned using a consistent `Response` object structure.
"""

from utils import log_msg, logging
from exc import AuthenticationException, CommonPYDBException, err_msg, codes

from .action import Action
from .storage import Storage
from .response import Response
from .constants import ActionEnum
from .auth import authentication


class PyDB:
    """
    Handles execution of database operations based on an Action object.

    This class serves as the main interface for interpreting incoming actions
    and executing corresponding logic using the underlying storage engine.
    """

    def __init__(self, action: Action):
        """
        Initialize PyDB with an action to process.

        Args:
            action (Action): Parsed action object containing command, data, and metadata.
        """
        self._action = action
        self._storage_engine = Storage()

        log_msg(logging.DEBUG, str(self._action))

    def run(self):
        """
        Execute the provided action and return a response.

        Returns:
            Response: Result of the action in serialized format.
        """
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
        """
        Handle the CREATE_TABLE action.

        Returns:
            Response: Confirmation with created table path or name.
        """
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
        """
        Handle the CREATE action to insert a new row into a table.

        Returns:
            Response: Inserted data and table name.

        Raises:
            CommonPYDBException: If table is not provided.
        """
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
        """
        Handle the UPDATE action to modify existing rows.

        Returns:
            Response: Count of affected rows.
        """
        effected_rows_count = self._storage_engine.update(
            table=self._action.table,
            query=self._action.query,
            update_data=self._action.payload,
            database=self._action.user_db_conf["NAME"],
        )

        return Response(
            act_type=ActionEnum.UPDATE,
            resp_payload={"count": effected_rows_count},
        )

    def delete(self):
        """
        Handle the DELETE action to remove rows matching a query.

        Returns:
            Response: Count of remaining rows after deletion.
        """
        effected_rows_count = self._storage_engine.delete(
            table=self._action.table,
            query=self._action.query,
            database=self._action.user_db_conf["NAME"],
        )
        return Response(
            act_type=ActionEnum.DELETE,
            resp_payload={"count": effected_rows_count},
        )

    def select(self):
        """
        Handle the SELECT action to retrieve matching rows from a table.

        Returns:
            Response: List of rows matching the query.
        """
        results = self._storage_engine.read(
            table=self._action.table,
            query=self._action.query,
            database=self._action.user_db_conf["NAME"],
        )

        return Response(
            act_type=ActionEnum.SELECT,
            resp_payload=results,
        )

    def create_database(self):
        """
        Handle the CREATE_DATABASE action.

        Returns:
            Response: Original database configuration on success.
        """
        self._storage_engine.create_database(self._action.payload)

        return Response(
            act_type=ActionEnum.CREATE_DATABASE,
            resp_payload=self._action.payload,
        )

    def drop_table(self):
        """
        Handle the DROP_TABLE action to delete a table.

        Returns:
            Response: Empty payload upon success.
        """
        self._storage_engine.drop_table(
            table=self._action.table,
            database=self._action.user_db_conf["NAME"],
        )
        return Response(
            act_type=ActionEnum.DROP_TABLE,
            resp_payload={},
        )

    def login(self):
        """
        Handle the LOGIN action by validating credentials and issuing a token.

        Returns:
            Response: Authentication token payload.

        Raises:
            AuthenticationException: If username or password is invalid.
        """
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
