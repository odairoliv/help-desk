class NotFoundError(Exception):
    """Recurso solicitado não existe."""


class BadRequestError(Exception):
    """Requisição malformada ou com regra de negócio violada."""
