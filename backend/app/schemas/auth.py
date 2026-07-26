"""Модуль  содержащий схемы сущности  auth."""

from pydantic import BaseModel


class TokenResponseSchema(BaseModel):
    """Схема для получения токена при авторизации."""

    auth_token: str
