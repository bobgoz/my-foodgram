"""Модуль с моделью Корзина  покупок."""

from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from async_foodgram.app.database import Base

from .mixins import PrimaryKeyMixin


class ShoppingCartModel(PrimaryKeyMixin, Base):
    """Модель список покупок."""

    __tablename__ = 'shopping_cart'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    user: Mapped['UserModel'] = relationship(back_populates='shopping_cart')
    recipe: Mapped['RecipeModel'] = relationship(
        back_populates='shopping_cart'
    )

    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'recipe_id',
            name='unique_shoping_cart',
        ),
    )
