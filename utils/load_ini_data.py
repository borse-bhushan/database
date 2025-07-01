from py_db.db import PyDB
from py_db.action import Action
from py_db.constants import ActionEnum


def load_ini_data_in_database(database_conf: list):

    for db_conf in database_conf:
        action = Action(
            payload=db_conf,
            action=ActionEnum.CREATE_DATABASE,
        )

        database = PyDB(action)
        database.create_database()
