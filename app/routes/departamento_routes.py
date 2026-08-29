from flask import Blueprint, jsonify, request

from app.schemas.departamento_schema import DepartamentoSchema, DepartamentoUpdateSchema
from app.services import departamento_service

departamento_bp = Blueprint("departamentos", __name__, url_prefix="/departamentos")

schema = DepartamentoSchema()
update_schema = DepartamentoUpdateSchema()


@departamento_bp.get("")
def listar_departamentos():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    nome = request.args.get("nome")

    paginacao = departamento_service.listar(page, per_page, nome)
    return jsonify(
        {
            "items": schema.dump(paginacao.items, many=True),
            "page": paginacao.page,
            "per_page": paginacao.per_page,
            "total": paginacao.total,
            "pages": paginacao.pages,
        }
    ), 200


@departamento_bp.get("/<int:departamento_id>")
def obter_departamento(departamento_id):
    departamento = departamento_service.obter(departamento_id)
    return jsonify(schema.dump(departamento)), 200


@departamento_bp.post("")
def criar_departamento():
    dados = schema.load(request.get_json(force=True, silent=True) or {})
    departamento = departamento_service.criar(dados)
    return jsonify(schema.dump(departamento)), 201


@departamento_bp.put("/<int:departamento_id>")
def substituir_departamento(departamento_id):
    dados = schema.load(request.get_json(force=True, silent=True) or {})
    departamento = departamento_service.atualizar(departamento_id, dados)
    return jsonify(schema.dump(departamento)), 200


@departamento_bp.patch("/<int:departamento_id>")
def atualizar_departamento(departamento_id):
    dados = update_schema.load(
        request.get_json(force=True, silent=True) or {}, partial=True
    )
    departamento = departamento_service.atualizar(departamento_id, dados, parcial=True)
    return jsonify(schema.dump(departamento)), 200


@departamento_bp.delete("/<int:departamento_id>")
def remover_departamento(departamento_id):
    departamento_service.remover(departamento_id)
    return "", 204
