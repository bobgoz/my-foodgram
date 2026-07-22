from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

from backend.app.models.associations import recipe_ingredient
from backend.app.models.constants import (
    MAX_LENGTH_MEASUREMENT_UNIT,
    MAX_LENGTH_NAME,
)
from backend.app.models.mixins import PrimaryKeyMixin


class IngredientModel(Base, PrimaryKeyMixin):
    """Модель Ингредиента"""

    __tablename__ = 'ingredients'
    name: Mapped[str] = mapped_column(String(MAX_LENGTH_NAME), nullable=False)
    measurement_unit: Mapped[str] = mapped_column(
        String(MAX_LENGTH_MEASUREMENT_UNIT),
        nullable=False,
    )
    recipes: Mapped[list['RecipeModel']] = relationship(
        secondary=recipe_ingredient,
        back_populates='ingredients',
    )
