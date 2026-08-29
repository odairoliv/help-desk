from app.extensions import db


class Departamento(db.Model):
    __tablename__ = "departamentos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    responsavel = db.Column(db.String(100), nullable=False)

    chamados = db.relationship(
        "Chamado",
        backref="departamento",
        lazy=True,
        cascade="all, delete-orphan",
    )
