from marshmallow import Schema, fields, validate

from app.models.chamado import PRIORIDADES, STATUS
from app.schemas.comentario_schema import ComentarioSchema


class ChamadoSchema(Schema):
    id = fields.Integer(dump_only=True)
    titulo = fields.String(required=True, validate=validate.Length(min=3, max=150))
    descricao = fields.String(required=True, validate=validate.Length(min=3))
    prioridade = fields.String(
        load_default="baixa", validate=validate.OneOf(PRIORIDADES)
    )
    status = fields.String(load_default="aberto", validate=validate.OneOf(STATUS))
    departamento_id = fields.Integer(required=True)
    criado_em = fields.DateTime(dump_only=True)
    comentarios = fields.Nested(ComentarioSchema, many=True, dump_only=True)


class ChamadoUpdateSchema(Schema):
    titulo = fields.String(validate=validate.Length(min=3, max=150))
    descricao = fields.String(validate=validate.Length(min=3))
    prioridade = fields.String(validate=validate.OneOf(PRIORIDADES))
    status = fields.String(validate=validate.OneOf(STATUS))
    departamento_id = fields.Integer()
