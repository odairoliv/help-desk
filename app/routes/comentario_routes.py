from flask import Blueprint, jsonify, request

from app.schemas.comentario_schema import ComentarioSchema
from app.services import comentario_service

comentario_bp = Blueprint(
    "comentarios", __name__, url_prefix="/chamados/<int:chamado_id>/comentarios"
)

schema = ComentarioSchema()


@comentario_bp.get("")
def listar_comentarios(chamado_id):
    comentarios = comentario_service.listar(chamado_id)
    return jsonify(schema.dump(comentarios, many=True)), 200


@comentario_bp.post("")
def criar_comentario(chamado_id):
    dados = schema.load(request.get_json(force=True, silent=True) or {})
    comentario = comentario_service.criar(chamado_id, dados)
    return jsonify(schema.dump(comentario)), 201


@comentario_bp.delete("/<int:comentario_id>")
def remover_comentario(chamado_id, comentario_id):
    comentario_service.remover(chamado_id, comentario_id)
    return "", 204
