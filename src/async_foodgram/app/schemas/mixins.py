"""Модуль, содержащий миксины для схем."""

from typing import Generic, TypeVar

from pydantic import BaseModel, HttpUrl

T = TypeVar('T')


class BasePaginationResponse(BaseModel, Generic[T]):
    """Базовая схема пагинированного списка."""

    count: int
    next: str | None
    previous: str | None
    results: list[T]
