from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import BASE_DIR, settings

if settings.DEBUG:
    database_url = URL.create('sqlite', database=str(BASE_DIR / 'foodgram.db'))
else:
    database_url = settings.DATABASE_URL

engine = create_engine(database_url)


SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    """Базовый класс для моделей"""

    pass
