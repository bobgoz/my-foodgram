from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from async_foodgram.app.database import Base
from async_foodgram.app.models.associations import recipe_ingredient
from async_foodgram.app.models.constants import (
    MAX_LENGTH_MEASUREMENT_UNIT,
    MAX_LENGTH_NAME,
)
from async_foodgram.app.models.mixins import PrimaryKeyMixin


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
