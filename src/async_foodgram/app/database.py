from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import BASE_DIR, settings

if settings.DEBUG:
    engine = create_engine(f'sqlite://{BASE_DIR}/foodgram.db')
else:
    engine = create_engine(settings.DATABASE_URL)


SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    """Базовый класс для моделей"""

    pass
