from app.routes.departamento_routes import departamento_bp
from app.routes.chamado_routes import chamado_bp


def register_routes(app):
    app.register_blueprint(departamento_bp)
    app.register_blueprint(chamado_bp)
