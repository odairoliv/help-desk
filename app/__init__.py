from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.errors import BadRequestError, NotFoundError
from app.extensions import db, migrate


def create_app(config_object: str = "config.Config") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401 - garante que os modelos sejam registrados
    from app.routes import register_routes

    register_routes(app)
    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"error": "Erro de validação", "detalhes": error.messages}), 422

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error: NotFoundError):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(BadRequestError)
    def handle_bad_request_error(error: BadRequestError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        db.session.rollback()
        app.logger.exception(error)
        return jsonify({"error": "Erro interno no servidor"}), 500
