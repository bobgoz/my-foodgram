"""Модель для связи рецепта и ингредиента."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from async_foodgram.app.database import Base


class RecipeIngredientModel(Base):
    """Модель связи рецепта и ингредиента с количеством."""

    __tablename__ = 'recipe_ingredient'
    __table_args__ = {
        'extend_existing': True,
    }

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey('recipes.id'),
        primary_key=True,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey('ingredients.id'),
        primary_key=True,
    )
    amount: Mapped[int] = mapped_column(nullable=False)
    recipe: Mapped['RecipeModel'] = relationship(
        back_populates='recipe_ingredients',
    )
    ingredient: Mapped['IngredientModel'] = relationship()
