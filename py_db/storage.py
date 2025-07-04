import os
import json

from env import environment
from exc import (
    DatabaseAlreadyExist,
    TableDoesNotExist,
    DatabaseNotExist,
    TableAlreadyExist,
)

from .schema_gen import schema
from .singleton import SingletonMeta


class Storage(metaclass=SingletonMeta):

    def __init__(self):
        self._data_folder = environment["DATA_FOLDER"]

    def get_table_path(self, database_path, table, schema_path=False):
        ext = ".py" if schema_path else ".data"
        return database_path + "/" + table + ext

    def is_table_exist(self, database_path, table):

        table_path = self.get_table_path(database_path, table)

        if os.path.exists(table_path):
            return table_path

        return False

    def create_table(self, database: str, table: str, schema_def):
        db_path = self.is_db_exist(database)
        if not db_path:
            raise DatabaseNotExist(database)

        table_path = self.is_table_exist(db_path, table)

        if table_path:
            raise TableAlreadyExist(table)

        table_path = self.get_table_path(db_path, table)
        with open(table_path, "w") as file:
            pass

        schema.Schema().write_schema_class_to_file(
            class_name=table.title(),
            schema_def=schema_def,
            table=table,
            database=database,
        )

        return table_path

    def insert_data(self, database, table, data):

        db_path = self.is_db_exist(database)

        if not db_path:
            raise DatabaseNotExist(database)

        table_path = self.is_table_exist(db_path, table)

        if not table_path:
            raise TableDoesNotExist(table)

        TableSchema = schema.Schema().get_schema(database=database, table=table)

        try:
            TableSchema().load(data)
        except Exception as e:
            print(e)

        with open(table_path, "a") as file:

            if not "pk" in data:
                self.read()

            file.write(json.dumps(data) + "\n")

        return data

    def get_db_path(self, db_name):
        return self._data_folder + f"/{db_name}"

    def is_db_exist(self, db_name):
        db_path = self.get_db_path(db_name=db_name)

        if os.path.exists(db_path):
            return db_path

        return False

    def create_database(self, database_conf, exist_ok=False):

        if not os.path.exists(self._data_folder):
            os.mkdir(self._data_folder)

        db_path = self.is_db_exist(database_conf["NAME"])
        if db_path:
            if exist_ok:
                return db_path

            raise DatabaseAlreadyExist(database_conf["NAME"])

        os.mkdir(db_path)

        with open(db_path + "/db_conf.json", "w") as db_conf_file:
            json.dump(database_conf, db_conf_file)

        return True

    def read_db_conf(self, db_name):

        db_path = self.is_db_exist(db_name=db_name)
        if not db_path:
            raise DatabaseNotExist(db_name)

        with open(db_path + "/db_conf.json", "r") as db_conf_file:
            return json.load(db_conf_file)

        return False

    def query(self, data: dict, query: dict):

        if not query:
            return True

        for key, itm in query.items():

            if data[key] == itm:
                return True

            return False

    def read(self, database, table, query):
        db_path = self.is_db_exist(database)
        if not db_path:
            raise DatabaseNotExist(database)

        table_path = self.is_table_exist(db_path, table)
        if not table_path:
            raise TableDoesNotExist(table)

        results = []
        with open(table_path, "r") as table:

            for line in table.readlines():
                if not line:
                    continue

                json_data = json.loads(line)
                if not self.query(json_data, query):
                    continue

                results.append(json_data)

        return results
