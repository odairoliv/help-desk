from datetime import datetime

from app.extensions import db


class Comentario(db.Model):
    __tablename__ = "comentarios"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    chamado_id = db.Column(
        db.Integer, db.ForeignKey("chamados.id"), nullable=False
    )
