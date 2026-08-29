from datetime import datetime

from app.extensions import db

PRIORIDADES = ("baixa", "media", "alta")
STATUS = ("aberto", "em_andamento", "resolvido")


class Chamado(db.Model):
    __tablename__ = "chamados"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), nullable=False, default="baixa")
    status = db.Column(db.String(20), nullable=False, default="aberto")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    departamento_id = db.Column(
        db.Integer, db.ForeignKey("departamentos.id"), nullable=False
    )

    comentarios = db.relationship(
        "Comentario",
        backref="chamado",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Comentario.criado_em",
    )
