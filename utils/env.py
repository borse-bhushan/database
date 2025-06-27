"""
# File: utils/env.py
# Description: Utility module to handle environment data.
"""

import os
import sys
import json

from .arg_pars import parser
from exc import CommonPYDBException, codes, err_msg


class Environment:
    """
    A class to represent the environment data.
    """

    def __init__(self):
        self.__env = {}

    def __getitem__(self, key: str):
        """
        Get an item from the environment data using the key.

        Args:
            key (str): The key to get from the environment data.

        Returns:
            The value associated with the key.
        """
        return self.__env[key]

    def __new__(cls):
        """
        Create a new instance of the Environment class or return the existing instance.
        """

        if not hasattr(cls, "_instance"):
            cls._instance = super(Environment, cls).__new__(cls)
        return cls._instance

    def __str__(self):
        """
        Return a string representation of the environment data.
        """
        return json.dumps(self.__env, indent=4)

    def __read_file(self, file_path: str):
        """
        Read the content of a file and return it as a string.

        Args:
            file_path (str): The path to the file to read.

        Returns:
            str: The content of the file.
        """
        if not os.path.exists(file_path):
            raise CommonPYDBException(
                code=codes.CONFIG_FILE_NOT_FOUND,
                message=err_msg.CONFIG_FILE_NOT_FOUND.format(file_path=file_path),
                ref_data={
                    "file_path": file_path,
                },
            )

        with open(file_path, "r", encoding="UTF-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as exc:
                raise CommonPYDBException(
                    code=codes.INVALID_CONFIG_JSON_FILE,
                    message=err_msg.INVALID_CONFIG_JSON_FILE.format(
                        file_path=file_path
                    ),
                    ref_data={
                        "file_path": file_path,
                    },
                ) from exc

    def load(self):
        """
        Load environment data from a JSON file.
        """

        default_file = os.path.join(os.path.dirname(__file__), "env.json")
        self.__env.update(self.__read_file(default_file))

        e_file = getattr(parser, "e_file", None)
        print(e_file)
        if e_file:
            index = sys.argv.index("-e-file") + 1
            if index < len(sys.argv):
                file_path = sys.argv[index]
                self.__env.update(self.__read_file(file_path))
            else:
                raise CommonPYDBException(
                    code=codes.CONFIG_FILE_NOT_FOUND,
                    message=(
                        err_msg.CONFIG_FILE_NOT_FOUND.format(file_path=sys.argv[index])
                        if index < len(sys.argv)
                        else "None"
                    ),
                )


environment = Environment()
