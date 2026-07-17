"""Модуль содержащий фикстуры для сущности ingredient."""

from pytest import fixture

from backend.app.models import IngredientModel


@fixture
def ingredient_object(db_session):
    ingredient = IngredientModel(
        name='Борщ',
        measurement_unit='грамм',
    )
    db_session.add(ingredient)
    db_session.commit()
    db_session.refresh(ingredient)

    return ingredient


@fixture
def ingredients(db_session):
    """Создание 10 ингредиентов."""
    ingredients = [
        IngredientModel(
            name=f'Курица_{i}',
            measurement_unit='грамм',
        )
        for i in range(10)
    ]
    db_session.add_all(ingredients)
    db_session.commit()


@fixture
def ingredient_url():
    return '/ingredients'


@fixture
def ingredient_detail_url(ingredient_object):
    return f'/ingredients/{ingredient_object.id}'
