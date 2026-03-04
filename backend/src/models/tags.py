from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.models.mixins import PrimaryKeyMixin
from src.models.constants import MAX_LENGTH


class TagModel(PrimaryKeyMixin, Base):
    """Модель Тега"""

    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(MAX_LENGTH))
    slug: Mapped[str] = mapped_column(String(MAX_LENGTH),unique=True, nullable=True)
