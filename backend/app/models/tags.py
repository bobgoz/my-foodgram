from backend.app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from backend.app.models.mixins import PrimaryKeyMixin
from backend.app.models.constants import MAX_LENGTH


class TagModel(PrimaryKeyMixin, Base):
    """Модель Тега"""

    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(MAX_LENGTH))
    slug: Mapped[str] = mapped_column(String(MAX_LENGTH),unique=True, nullable=True)
