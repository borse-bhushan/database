"""
# Description: Exception classes for schema-related validation errors.
"""

from .base import BaseExc
from . import codes, err_msg


class FieldTypeError(BaseExc):
    """
    Raised when a schema field has an unsupported or unrecognized type.

    Attributes:
        code (str): Error code indicating field type issues.
        message (str): Error message template.

    Args:
        f_type (str, optional): The invalid field type.
        ref_data (dict, optional): Additional context information.
    """

    code = codes.FIELD_TYPE_NOT_AVAILABLE
    message = err_msg.FIELD_TYPE_NOT_AVAILABLE

    def __init__(self, f_type=None, ref_data=None):
        super().__init__(
            code=self.code,
            ref_data=ref_data,
            message=self.message.format(f_type=f_type),
        )


class FieldValidationError(BaseExc):
    """
    Raised when a field fails validation rules during schema processing.

    Attributes:
        code (str): Error code indicating a field validation problem.
        message (str): Error message template.

    Args:
        field (str): The name of the invalid field.
        f_type (str): The type of the field.
        ref_data (dict, optional): Additional context information.
    """

    code = codes.FIELD_VALIDATION_VALUE
    message = err_msg.FIELD_VALIDATION_VALUE

    def __init__(self, field, f_type, ref_data=None):
        super().__init__(
            code=self.code,
            ref_data=ref_data,
            message=self.message.format(f_type=f_type, field=field),
        )
