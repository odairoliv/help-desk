from marshmallow import Schema, fields, validate


class DepartamentoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nome = fields.String(required=True, validate=validate.Length(min=2, max=100))
    responsavel = fields.String(required=True, validate=validate.Length(min=2, max=100))


class DepartamentoUpdateSchema(Schema):
    nome = fields.String(validate=validate.Length(min=2, max=100))
    responsavel = fields.String(validate=validate.Length(min=2, max=100))
