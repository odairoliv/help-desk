from app.errors import NotFoundError
from app.extensions import db
from app.models.departamento import Departamento


def listar(page: int, per_page: int, nome: str | None):
    query = Departamento.query
    if nome:
        query = query.filter(Departamento.nome.ilike(f"%{nome}%"))
    return query.paginate(page=page, per_page=per_page, error_out=False)


def obter(departamento_id: int) -> Departamento:
    departamento = Departamento.query.get(departamento_id)
    if departamento is None:
        raise NotFoundError(f"Departamento {departamento_id} não encontrado")
    return departamento


def criar(dados: dict) -> Departamento:
    departamento = Departamento(**dados)
    db.session.add(departamento)
    db.session.commit()
    return departamento


def atualizar(departamento_id: int, dados: dict, parcial: bool = False) -> Departamento:
    departamento = obter(departamento_id)
    for campo, valor in dados.items():
        setattr(departamento, campo, valor)
    db.session.commit()
    return departamento


def remover(departamento_id: int) -> None:
    departamento = obter(departamento_id)
    db.session.delete(departamento)
    db.session.commit()
