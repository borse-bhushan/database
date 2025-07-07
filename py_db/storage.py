import os
import json

from env import environment
from exc import (
    DatabaseAlreadyExist,
    TableDoesNotExist,
    DatabaseNotExist,
    TableAlreadyExist,
    DataIsNotValid,
    UniqueValueFound,
    CommonPYDBException,
    err_msg,
    codes,
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

        table_schema_obj = schema.Schema().get_schema(database=database, table=table)()

        try:
            data = table_schema_obj.load(data)
        except Exception as e:
            raise DataIsNotValid(e.messages) from e

        unique_fields = getattr(table_schema_obj, "get_unique", None)

        data = table_schema_obj.dump(data)

        if callable(unique_fields):
            unique_fields = unique_fields()

        if unique_fields and isinstance(unique_fields, list):
            for field in unique_fields:
                result = self.read(
                    table=table, database=database, query={field: data[field]}
                )
                if result:
                    raise UniqueValueFound(field=field, value=data[field])

        with open(table_path, "a") as file:
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

    def drop_table(self, database, table):
        db_path = self.is_db_exist(database)

        if not db_path:
            raise DatabaseNotExist(database)

        table_path = self.is_table_exist(db_path, table)

        if not table_path:
            raise TableDoesNotExist(table)

        os.remove(table_path)
        schema.Schema().remove(database=database, table=table)

        return True

    def update(self, query, database, table, update_data):

        db_path = self.is_db_exist(database)
        if not db_path:
            raise DatabaseNotExist(database)

        table_path = self.is_table_exist(db_path, table)
        if not table_path:
            raise TableDoesNotExist(table)

        if "pk" in update_data:
            raise CommonPYDBException(
                code=codes.UPDATE_NOT_ALLOWED_ON_PK,
                message=err_msg.UPDATE_NOT_ALLOWED_ON_PK,
                ref_data={
                    "table": table,
                    "database": database,
                },
            )

        updated_data_lines = []

        TableSchema = schema.Schema().get_schema(database=database, table=table)

        table_schema = TableSchema()

        unique_fields = getattr(table_schema, "get_unique", [])

        validate_unique_fields = []
        if unique_fields and callable(unique_fields):

            for field in unique_fields():
                if field in update_data:
                    validate_unique_fields.append(field)

        with open(table_path, "r") as table_file:

            lines = table_file.readlines()

            for index, line in enumerate(lines):
                if not line:
                    continue

                json_data = json.loads(line)
                if not self.query(json_data, query):
                    continue

                if validate_unique_fields:
                    for field in validate_unique_fields:
                        data = self.read(
                            table=table,
                            database=database,
                            query={field: update_data[field]},
                        )

                        if data:
                            for row in data:
                                if row["pk"] != json_data["pk"]:
                                    raise UniqueValueFound(
                                        field=field, value=row[field]
                                    )

                json_data.update(update_data)

                table_schema_obj = schema.Schema().get_schema(
                    database=database, table=table
                )()

                try:
                    table_schema_obj.load(json_data, partial=True)
                except Exception as e:
                    raise DataIsNotValid(e.messages) from e

                updated_data_lines.append(json_data)
                lines[index] = json.dumps(json_data) + "\n"

        if updated_data_lines:
            with open(table_path, "w") as table_file:
                table_file.writelines(lines)

        return len(updated_data_lines)

    def delete(self, database, table, query):

        db_path = self.is_db_exist(database)
        if not db_path:
            raise DatabaseNotExist(database)

        table_path = self.is_table_exist(db_path, table)
        if not table_path:
            raise TableDoesNotExist(table)

        new_data = []
        with open(table_path, "r") as table_file:

            lines = table_file.readlines()

            for line in lines:
                if not line:
                    continue

                json_data = json.loads(line)
                if self.query(json_data, query):
                    continue

                new_data.append(line)

        if new_data:
            with open(table_path, "w") as table_file:
                table_file.writelines(new_data)

        return len(new_data)
