from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DATABASE_URL = f'sqlite:///{BASE_DIR}/foodgram.db'

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    """Базовый класс для моделей"""

    pass
