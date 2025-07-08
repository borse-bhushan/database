"""
Responsible for dynamically generating and managing Marshmallow schema classes
based on user-defined table definitions.

This module provides methods to:
- Load a schema class dynamically
- Remove schema files
- Generate Marshmallow field definitions with validations
- Write schema classes to Python files at runtime
"""

import os
import marshmallow
from importlib import import_module

from exc import TableSchemaNotExist


class Schema:
    """
    Handles dynamic schema generation and loading for table definitions using Marshmallow.

    Attributes:
        import_path (str): Template path for importing table schema modules.
        init_file (str): Path to the __init__.py for each database schema folder.
        table_schema (str): Path to the generated schema file for a specific table.
    """

    def __init__(self):
        self.import_path = "schema.{database}.{table}"
        self.init_file = "schema/{database}/__init__.py"
        self.table_schema = "schema/{database}/{table}.py"

    def get_schema(self, database, table) -> type[marshmallow.Schema]:
        """
        Dynamically import and return a Marshmallow schema class for the given table.

        Args:
            database (str): Name of the database.
            table (str): Name of the table.

        Returns:
            Type[marshmallow.Schema]: The schema class for the table.

        Raises:
            TableSchemaNotExist: If the schema file or class does not exist.
        """
        try:
            return getattr(
                import_module(self.import_path.format(database=database, table=table)),
                table.title(),
            )
        except ImportError as exe:
            raise TableSchemaNotExist(table) from exe

    def remove(self, database, table):
        """
        Delete the schema file for a specific table.

        Args:
            database (str): Name of the database.
            table (str): Name of the table.

        Returns:
            bool: True if the file was successfully removed.
        """
        os.remove(self.table_schema.format(database=database, table=table))
        return True

    def generate_marshmallow_field_code(self, field_name, field_spec):
        """
        Generate the Marshmallow field definition string from a field spec.

        Args:
            field_name (str): Name of the field.
            field_spec (dict): Field specification including type, validations, etc.

        Returns:
            str: Marshmallow-compatible Python code defining the field.
        """
        type_map = {
            "str": "fields.Str",
            "int": "fields.Int",
            "float": "fields.Float",
            "bool": "fields.Bool",
            "date": "fields.Date",
            "datetime": "fields.DateTime",
            "uuid": "fields.UUID",
        }

        marshmallow_type = type_map.get(field_spec["type"])
        if not marshmallow_type:
            raise ValueError(f"Unsupported type: {field_spec['type']}")

        required = field_spec.get("required", False)
        allow_none = field_spec.get("allow_none", False)
        default = field_spec.get("default")
        callable_default = field_spec.get("callable_default")
        validators = []

        parts = [f"{field_name} = {marshmallow_type}("]

        if field_spec["type"] == "str":
            if "min_length" in field_spec or "max_length" in field_spec:
                validators.append(
                    f"validate.Length(min={field_spec.get('min_length', 0)}, max={field_spec.get('max_length', 'None')})"
                )
            if "pattern" in field_spec:
                validators.append(f"validate.Regexp(r'{field_spec['pattern']}')")
            if "enum" in field_spec:
                validators.append(f"validate.OneOf({field_spec['enum']})")

        elif field_spec["type"] in ["int", "float"]:
            if "min" in field_spec or "max" in field_spec:
                validators.append(
                    f"validate.Range(min={field_spec.get('min')}, max={field_spec.get('max')})"
                )
            if "enum" in field_spec:
                validators.append(f"validate.OneOf({field_spec['enum']})")

        elif field_spec["type"] == "datetime":
            parts.append(f"    format='{field_spec.get('format', 'iso')}',")

        validator_str = f"[{', '.join(validators)}]" if validators else "None"

        parts.append(f"    required={required},")
        parts.append(f"    allow_none={allow_none},")

        if default is not None:
            parts.append(f"    load_default={repr(default)},")
            parts.append(f"    dump_default={repr(default)},")

        if callable_default is not None:
            parts.append(f"    load_default={callable_default},")
            parts.append(f"    dump_default={callable_default},")

        if validators:
            parts.append(f"    validate={validator_str},")
        parts.append(")")
        return "\n".join(parts)

    def generate_validators(self, schema_def):
        """
        Generate code for the `get_unique` method based on schema uniqueness constraints.

        Args:
            schema_def (dict): Schema field definitions.

        Returns:
            list[str]: Lines of Python code defining the get_unique method.
        """
        lines = []
        unique_fields = []
        for field_name, spec in schema_def.items():
            if spec.get("unique", False):
                unique_fields.append(f"'{field_name}'")
        lines.append(f"    def get_unique(self):")
        lines.append(f"        return [{', '.join(unique_fields)}]")

        return lines

    def write_schema_class_to_file(self, class_name, schema_def, database, table):
        """
        Generate and write a complete Marshmallow schema class to a Python file.

        Args:
            class_name (str): The name of the schema class.
            schema_def (dict): Dictionary of field definitions.
            database (str): Target database name.
            table (str): Target table name.
        """
        file_path = self.table_schema.format(database=database, table=table)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        lines = [
            "from marshmallow import Schema, fields, validate, validates, ValidationError\n",
            "from utils.comm_fun import get_uuid",
            f"class {class_name}(Schema):",
        ]

        schema_def["pk"] = {
            "type": "uuid",
            "unique": True,
            "callable_default": "get_uuid",
        }

        for field_name, spec in schema_def.items():
            field_code = self.generate_marshmallow_field_code(field_name, spec)
            lines.append("    " + field_code.replace("\n", "\n    "))

        validator_lines = self.generate_validators(schema_def)
        if validator_lines:
            lines.append("")
            lines.extend(validator_lines)

        with open(file_path, "w") as f:
            f.write("\n".join(lines))

        with open(self.init_file.format(database=database, table=table), "w") as f:
            f.write("")
