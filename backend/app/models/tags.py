from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

# from .recipes import RecipeModel, recipe_tag
from backend.app.models.associations import recipe_tag
from backend.app.models.constants import MAX_LENGTH
from backend.app.models.mixins import PrimaryKeyMixin


class TagModel(PrimaryKeyMixin, Base):
    """Модель Тега"""

    __tablename__ = 'tags'
    name: Mapped[str] = mapped_column(String(MAX_LENGTH))
    slug: Mapped[str] = mapped_column(
        String(MAX_LENGTH), unique=True, nullable=True
    )
    recipes: Mapped[list['RecipeModel']] = relationship(
        secondary=recipe_tag,
        back_populates='tags',
    )
