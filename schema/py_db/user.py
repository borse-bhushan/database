from marshmallow import Schema, fields, validate, validates, ValidationError

from utils.comm_fun import get_uuid


class User(Schema):
    first_name = fields.Str(
        required=True,
        allow_none=False,
        validate=[validate.Length(min=2, max=20), validate.Regexp(r"^[a-zA-Z]+$")],
    )
    age = fields.Int(
        required=True,
        allow_none=False,
        validate=[validate.Range(min=18, max=99)],
    )
    pk = fields.UUID(
        required=False,
        allow_none=False,
        load_default=get_uuid,
        dump_default=get_uuid,
    )

    def get_unique(self):
        return ["first_name", "age", "pk"]
