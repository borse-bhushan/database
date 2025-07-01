import os
import json

from env import environment
from exc import DatabaseAlreadyExist
from .singleton import SingletonMeta


class Storage(metaclass=SingletonMeta):

    def __init__(self):
        self._data_folder = environment["DATA_FOLDER"]

    def write_data_to_disk(self, database, table, data):
        pass

    def read_data_from_block(self, database, table, data):
        pass

    def create_database(self, database_conf):

        if not os.path.exists(self._data_folder):
            os.mkdir(self._data_folder)

        db_name = database_conf["NAME"]
        db_path = self._data_folder + f"/{db_name}"

        if os.path.exists(db_path):
            raise DatabaseAlreadyExist(db_name)

        os.mkdir(db_path)

        with open(db_path + "/db_conf.json", "w") as auth_file:
            json.dump(database_conf, auth_file)

        return True
