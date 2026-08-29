from app.errors import NotFoundError
from app.extensions import db
from app.models.comentario import Comentario
from app.services.chamado_service import obter as obter_chamado


def listar(chamado_id: int):
    obter_chamado(chamado_id)
    return Comentario.query.filter_by(chamado_id=chamado_id).order_by(Comentario.criado_em).all()


def criar(chamado_id: int, dados: dict) -> Comentario:
    obter_chamado(chamado_id)
    comentario = Comentario(chamado_id=chamado_id, **dados)
    db.session.add(comentario)
    db.session.commit()
    return comentario


def obter(chamado_id: int, comentario_id: int) -> Comentario:
    comentario = Comentario.query.filter_by(id=comentario_id, chamado_id=chamado_id).first()
    if comentario is None:
        raise NotFoundError(f"Comentário {comentario_id} não encontrado")
    return comentario


def remover(chamado_id: int, comentario_id: int) -> None:
    comentario = obter(chamado_id, comentario_id)
    db.session.delete(comentario)
    db.session.commit()
