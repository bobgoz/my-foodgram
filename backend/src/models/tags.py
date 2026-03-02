from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

MAX_LENGTH = 32


class PrimaryKeyMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class TagModel(PrimaryKeyMixin, Base):
    """Модель Тега"""

    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(MAX_LENGTH))
    slug: Mapped[str] = mapped_column(String(MAX_LENGTH), nullable=True)
