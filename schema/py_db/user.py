from marshmallow import Schema, fields, validate, validates, ValidationError

class User(Schema):
    first_name = fields.Str(
        required=True,
        allow_none=False,
        validate=[validate.Length(min=2, max=20), validate.Regexp(r'^[a-zA-Z]+$')],
    )
    age = fields.Int(
        required=True,
        allow_none=False,
        validate=[validate.Range(min=18, max=99)],
    )
    salary = fields.Float(
        required=False,
        allow_none=False,
        validate=[validate.Range(min=0.0, max=None)],
    )
    is_active = fields.Bool(
        required=False,
        allow_none=False,
        load_default=True,
        dump_default=True,
    )
    join_date = fields.Date(
        required=True,
        allow_none=False,
    )
    last_login = fields.DateTime(
        required=False,
        allow_none=False,
    )

    def get_unique(self):
        return ['first_name', 'age']