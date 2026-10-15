"""Модуль, содержащий методы для пагинации."""

from fastapi import Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def paginate_query(
    session: Session,
    statement,
    request: Request,
    page: int,
    limit: int,
) -> dict:
    count_query = select(func.count()).select_from(
        statement.order_by(None).subquery()
    )
    count = session.scalar(count_query) or 0

    results = session.scalars(
        statement.offset((page - 1) * limit).limit(limit)
    ).all()

    next_url = (
        str(
            request.url.include_query_params(
                page=page + 1,
                limit=limit,
            )
        )
        if page * limit < count
        else None
    )
    previous_url = (
        str(
            request.url.include_query_params(
                page=page - 1,
                limit=limit,
            )
        )
        if page > 1
        else None
    )

    return {
        'count': count,
        'next': next_url,
        'previous': previous_url,
        'results': results,
    }
