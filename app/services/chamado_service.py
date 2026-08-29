from app.errors import BadRequestError, NotFoundError
from app.extensions import db
from app.models.chamado import Chamado
from app.models.departamento import Departamento


def _validar_departamento(departamento_id: int) -> None:
    if departamento_id is not None and not Departamento.query.get(departamento_id):
        raise BadRequestError(f"Departamento {departamento_id} não existe")


def listar(page: int, per_page: int, status: str | None, prioridade: str | None, departamento_id: int | None):
    query = Chamado.query
    if status:
        query = query.filter(Chamado.status == status)
    if prioridade:
        query = query.filter(Chamado.prioridade == prioridade)
    if departamento_id:
        query = query.filter(Chamado.departamento_id == departamento_id)
    return query.paginate(page=page, per_page=per_page, error_out=False)


def obter(chamado_id: int) -> Chamado:
    chamado = Chamado.query.get(chamado_id)
    if chamado is None:
        raise NotFoundError(f"Chamado {chamado_id} não encontrado")
    return chamado


def criar(dados: dict) -> Chamado:
    _validar_departamento(dados.get("departamento_id"))
    chamado = Chamado(**dados)
    db.session.add(chamado)
    db.session.commit()
    return chamado


def atualizar(chamado_id: int, dados: dict) -> Chamado:
    chamado = obter(chamado_id)
    if "departamento_id" in dados:
        _validar_departamento(dados["departamento_id"])
    for campo, valor in dados.items():
        setattr(chamado, campo, valor)
    db.session.commit()
    return chamado


def remover(chamado_id: int) -> None:
    chamado = obter(chamado_id)
    db.session.delete(chamado)
    db.session.commit()
