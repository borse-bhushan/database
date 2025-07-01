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

    def get_db_path(self, db_name):
        return self._data_folder + f"/{db_name}"

    def db_exist(self, db_name, not_exist_ok=True):
        db_path = self.get_db_path(db_name=db_name)

        if os.path.exists(db_path):
            return db_path

        if not_exist_ok:
            return False

        raise DatabaseAlreadyExist(db_name)

    def create_database(self, database_conf):

        if not os.path.exists(self._data_folder):
            os.mkdir(self._data_folder)

        db_path = self.db_exist(database_conf["NAME"])

        os.mkdir(db_path)

        with open(db_path + "/db_conf.json", "w") as db_conf_file:
            json.dump(database_conf, db_conf_file)

        return True

    def read_db_conf(self, db_name):
        db_path = self.db_exist(db_name=db_name, not_exist_ok=False)

        with open(db_path + "/db_conf.json", "r") as db_conf_file:
            return json.load(db_conf_file)

        return False
