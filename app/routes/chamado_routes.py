from flask import Blueprint, jsonify, request

from app.schemas.chamado_schema import ChamadoSchema, ChamadoUpdateSchema
from app.services import chamado_service

chamado_bp = Blueprint("chamados", __name__, url_prefix="/chamados")

schema = ChamadoSchema()
update_schema = ChamadoUpdateSchema()


@chamado_bp.get("")
def listar_chamados():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status")
    prioridade = request.args.get("prioridade")
    departamento_id = request.args.get("departamento_id", type=int)

    paginacao = chamado_service.listar(page, per_page, status, prioridade, departamento_id)
    return jsonify(
        {
            "items": schema.dump(paginacao.items, many=True),
            "page": paginacao.page,
            "per_page": paginacao.per_page,
            "total": paginacao.total,
            "pages": paginacao.pages,
        }
    ), 200


@chamado_bp.get("/<int:chamado_id>")
def obter_chamado(chamado_id):
    chamado = chamado_service.obter(chamado_id)
    return jsonify(schema.dump(chamado)), 200


@chamado_bp.post("")
def criar_chamado():
    dados = schema.load(request.get_json(force=True, silent=True) or {})
    chamado = chamado_service.criar(dados)
    return jsonify(schema.dump(chamado)), 201


@chamado_bp.put("/<int:chamado_id>")
def substituir_chamado(chamado_id):
    dados = schema.load(request.get_json(force=True, silent=True) or {})
    chamado = chamado_service.atualizar(chamado_id, dados)
    return jsonify(schema.dump(chamado)), 200


@chamado_bp.patch("/<int:chamado_id>")
def atualizar_chamado(chamado_id):
    dados = update_schema.load(
        request.get_json(force=True, silent=True) or {}, partial=True
    )
    chamado = chamado_service.atualizar(chamado_id, dados)
    return jsonify(schema.dump(chamado)), 200


@chamado_bp.delete("/<int:chamado_id>")
def remover_chamado(chamado_id):
    chamado_service.remover(chamado_id)
    return "", 204
