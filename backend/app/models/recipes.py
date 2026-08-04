from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base

from .associations import recipe_ingredient, recipe_tag

# from .ingredients import IngredientModel
from .mixins import PrimaryKeyMixin


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
    ingredients: Mapped[list['IngredientModel']] = relationship(
        secondary=recipe_ingredient, back_populates='recipes'
    )

    tags: Mapped[list['TagModel']] = relationship(
        secondary=recipe_tag,
        back_populates='recipes',
    )
    author_id: Mapped[int] = mapped_column(
        (
            ForeignKey(
                'users.id',
                name='fk_recipes_users',
            )
        )
    )
    author: Mapped['UserModel'] = relationship(
        back_populates='recipes',
    )
    shopping_cart: Mapped[list['ShoppingCartModel']] = relationship(
        back_populates='recipe',
        cascade='all, delete',
    )
