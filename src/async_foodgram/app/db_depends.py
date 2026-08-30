from collections.abc import Generator

from sqlalchemy.orm import Session

from async_foodgram.app.database import SessionLocal


def get_session() -> Generator[Session, None, None]:
    """Получение сессии для работы с БД"""
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
