from inspect import isclass
from typing import Union, Collection

from dataclasses import dataclass, is_dataclass, asdict
from marshmallow import SchemaOpts, Schema, post_load, validates_schema, ValidationError, fields
from sanic.http import STATUS_CODES

try:
    import rapidjson as json_module
except ImportError:
    try:
        import ujson as json_module
    except ImportError:
        import json as json_module


class DataClassOpts(SchemaOpts):
    def __init__(self, meta):
        super().__init__(meta)
        self.dataclass = getattr(meta, 'dataclass', None)


class SchemaError(Exception):
    pass


class BaseSchema(Schema):
    OPTIONS_CLASS = DataClassOpts

    class Meta:
        render_module = json_module
        dataclass = None

    @post_load
    def load_model(self, data):
        if not (isclass(self.opts.dataclass) and is_dataclass(self.opts.dataclass)):
            raise SchemaError('`Meta.dataclass` is not actually python dataclass')

        return self.opts.dataclass(**data)

    @validates_schema
    def not_none(self, data):
        if data is None:
            raise ValidationError('Data must be not empty')


@dataclass(frozen=True)
class ErrorModel(Exception):
    code: int
    message: Union[str, Collection]

    @classmethod
    def ok(cls):
        return cls(code=200, message='OK')

    @property
    def args(self):
        return self.code, self.message

    @property
    def status_code(self):
        if self.code in STATUS_CODES:
            return self.code

        return 500

    def __hash__(self):
        import json
        return hash(json.dumps(asdict(self)))


class ErrorModelSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        dataclass = ErrorModel

    code = fields.Integer(required=True)
    message = fields.Raw(required=True)


class InputSchema(Schema):
    def handle_error(self, error: ValidationError, data):
        msg = {'summary': 'There are errors in input data', 'errors': error.messages}

        raise ErrorModel(code=400, message=msg)
