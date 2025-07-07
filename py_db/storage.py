"""
This module defines the Storage class responsible for managing the persistent storage
of a custom Python-based file system database. It provides functionality for creating
databases and tables, reading and writing data, enforcing schema validation and uniqueness,
and supporting MongoDB-like queries.

It follows a singleton pattern to ensure consistent state and configuration.
"""

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
    """
    Handles all file-based storage operations for the custom database engine.
    Supports database/table creation, record-level operations, schema validation,
    uniqueness enforcement, and basic query matching.
    """

    def __init__(self):
        """
        Initialize the storage manager by retrieving the configured data folder path.
        """
        self._data_folder = environment["DATA_FOLDER"]

    def get_table_path(self, database_path, table, schema_path=False):
        """
        Construct the full file path for a table.

        Args:
            database_path (str): Path to the database folder.
            table (str): Table name.
            schema_path (bool): Whether to return the schema file path.

        Returns:
            str: Full file path to the table's data or schema file.
        """
        ext = ".py" if schema_path else ".data"
        return database_path + "/" + table + ext

    def is_table_exist(self, database_path, table):
        """
        Check if a table file exists.

        Args:
            database_path (str): Path to the database.
            table (str): Table name.

        Returns:
            str or bool: Path to the table if it exists, else False.
        """
        table_path = self.get_table_path(database_path, table)

        if os.path.exists(table_path):
            return table_path

        return False

    def create_table(self, database: str, table: str, schema_def):
        """
        Create a new table and its schema in a given database.

        Args:
            database (str): Database name.
            table (str): Table name.
            schema_def (dict): Schema definition for the table.

        Returns:
            str: Path to the created table file.

        Raises:
            DatabaseNotExist: If the database doesn't exist.
            TableAlreadyExist: If the table already exists.
        """
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
        """
        Validate and insert a row of data into the specified table.

        Args:
            database (str): Database name.
            table (str): Table name.
            data (dict): Record data to insert.

        Returns:
            dict: Validated and written data.

        Raises:
            Various validation exceptions including:
            - DatabaseNotExist
            - TableDoesNotExist
            - DataIsNotValid
            - UniqueValueFound
        """
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
        """
        Construct full path to a database folder.

        Args:
            db_name (str): Name of the database.

        Returns:
            str: Full path to the database.
        """
        return self._data_folder + f"/{db_name}"

    def is_db_exist(self, db_name):
        """
        Check whether the specified database exists.

        Args:
            db_name (str): Name of the database.

        Returns:
            str or bool: Path if exists, else False.
        """
        db_path = self.get_db_path(db_name=db_name)

        if os.path.exists(db_path):
            return db_path

        return False

    def create_database(self, database_conf, exist_ok=False):
        """
        Create a new database directory and config file.

        Args:
            database_conf (dict): Configuration dictionary (must include "NAME").
            exist_ok (bool): If True, return path if DB exists instead of raising.

        Returns:
            bool or str: True on success or path if exist_ok=True and DB already exists.

        Raises:
            DatabaseAlreadyExist: If DB exists and exist_ok=False.
        """
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
        """
        Load the config for a given database.

        Args:
            db_name (str): Name of the database.

        Returns:
            dict: Database configuration.

        Raises:
            DatabaseNotExist: If the database does not exist.
        """
        db_path = self.is_db_exist(db_name=db_name)
        if not db_path:
            raise DatabaseNotExist(db_name)

        with open(db_path + "/db_conf.json", "r") as db_conf_file:
            return json.load(db_conf_file)

        return False

    def match_condition(self, value, condition):
        """
        Evaluate a value against a query condition using MongoDB-style operators.

        Supported: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin

        Args:
            value: Field value from the row.
            condition (dict or value): Query condition.

        Returns:
            bool: Whether the condition matches.
        """
        if isinstance(condition, dict):
            for op, cond_val in condition.items():
                if op == "$eq":
                    if value != cond_val:
                        return False
                elif op == "$ne":
                    if value == cond_val:
                        return False
                elif op == "$gt":
                    if value <= cond_val:
                        return False
                elif op == "$gte":
                    if value < cond_val:
                        return False
                elif op == "$lt":
                    if value >= cond_val:
                        return False
                elif op == "$lte":
                    if value > cond_val:
                        return False
                elif op == "$in":
                    if value not in cond_val:
                        return False
                elif op == "$nin":
                    if value in cond_val:
                        return False
                else:
                    raise ValueError(f"Unsupported operator: {op}")
            return True
        else:
            return value == condition

    def query(self, row: dict, query: dict) -> bool:
        """
        Match a row against a query using MongoDB-like filtering.

        Args:
            row (dict): The row to evaluate.
            query (dict): Query filters.

        Returns:
            bool: True if the row matches the query, else False.
        """
        if not query:
            return True

        for key, condition in query.items():
            if key not in row:
                return False

            if not self.match_condition(row[key], condition):
                return False

        return True

    def read(self, database, table, query):
        """
        Read and return all rows from a table that match a query.

        Args:
            database (str): Database name.
            table (str): Table name.
            query (dict): Query filters.

        Returns:
            list: List of matching rows.
        """
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
        """
        Remove a table and its associated schema.

        Args:
            database (str): Database name.
            table (str): Table name.

        Returns:
            bool: True on successful deletion.
        """
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
        """
        Update matching rows with new data.

        Args:
            query (dict): Query filter to find target rows.
            database (str): Database name.
            table (str): Table name.
            update_data (dict): Data to update in matched rows.

        Returns:
            int: Number of rows updated.

        Raises:
            CommonPYDBException: If trying to update the primary key.
            UniqueValueFound: If new values violate unique constraints.
            DataIsNotValid: If updated data fails schema validation.
        """
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
        """
        Delete rows matching a query from the table.

        Args:
            database (str): Database name.
            table (str): Table name.
            query (dict): Filter to identify rows to delete.

        Returns:
            int: Number of remaining rows after deletion.
        """
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
