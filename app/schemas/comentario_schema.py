from marshmallow import Schema, fields, validate


class ComentarioSchema(Schema):
    id = fields.Integer(dump_only=True)
    texto = fields.String(required=True, validate=validate.Length(min=1))
    autor = fields.String(required=True, validate=validate.Length(min=2, max=100))
    chamado_id = fields.Integer(dump_only=True)
    criado_em = fields.DateTime(dump_only=True)
