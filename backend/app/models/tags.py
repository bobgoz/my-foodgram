from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.models.constants import MAX_LENGTH
from backend.app.models.mixins import PrimaryKeyMixin

from .recipes import RecipeModel, recipe_tag


class TagModel(PrimaryKeyMixin, Base):
    """Модель Тега"""

    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(MAX_LENGTH))
    slug: Mapped[str] = mapped_column(
        String(MAX_LENGTH), unique=True, nullable=True
    )
    recipes: Mapped[list['RecipeModel']] = mapped_column(
        relationship(
            secondary=recipe_tag,
            back_populates='tags',
        )
    )
