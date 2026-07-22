from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

from .ingredients import IngredientModel
from .mixins import PrimaryKeyMixin
from .tags import TagModel



class RecipeModel(
    Base,
    PrimaryKeyMixin,
):
    """Модель рецепта."""

    __tablename__ = 'recipes'
    name: Mapped[str] = mapped_column(String(100))
    text: Mapped[str] = mapped_column(String(100))
    cooking_time: Mapped[int] = mapped_column()
    image: Mapped[str] = mapped_column()
    ingredients: Mapped[list['IngredientModel']] = mapped_column(
        relationship(secondary=recipe_ingredient, back_populates='recipes'),
    )
    tags: Mapped[list['TagModel']] = mapped_column(
        relationship(secondary=recipe_tag, back_populates='recipes'),
    )
