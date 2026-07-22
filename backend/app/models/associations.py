"""Модуль, содержащий таблицы для связанных моделей Many-to-Many."""

from backend.app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

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
