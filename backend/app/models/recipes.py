from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

from .ingredients import IngredientModel
from .mixins import PrimaryKeyMixin
from .tags import TagModel

recipe_ingredient = Table(
    'recipe_ingredient',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column(
        'ingredient_id',
        Integer,
        ForeignKey('ingredients.id'),
        primary_key=True,
    ),
    Column('amount', Integer, nullable=False, default=1),
)

recipe_tag = Table(
    'recipe_tag',
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


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
        relationship(secondary=recipe_tag, back_populates='recipes'),
    )
    tags: Mapped[list['TagModel']] = mapped_column(
        relationship(secondary=recipe_tag, back_populates='recipes'),
    )
