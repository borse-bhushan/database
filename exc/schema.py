from .base import BaseExc
from . import codes, err_msg


class FieldTypeError(BaseExc):
    code = codes.FIELD_TYPE_NOT_AVAILABLE
    message = err_msg.FIELD_TYPE_NOT_AVAILABLE

    def __init__(self, f_type=None, ref_data=None):
        super().__init__(
            code=self.code,
            ref_data=ref_data,
            message=self.message.format(f_type=f_type),
        )


class FieldValidationError(BaseExc):
    code = codes.FIELD_VALIDATION_VALUE
    message = err_msg.FIELD_VALIDATION_VALUE

    def __init__(self, field, f_type, ref_data=None):
        super().__init__(
            code=self.code,
            ref_data=ref_data,
            message=self.message.format(f_type=f_type, field=field),
        )
