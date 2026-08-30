from pytest import fixture

from async_foodgram.app.models import IngredientModel


@fixture
def ingredient_object(db_session):
    """Объект ингредиента."""

    ingredient = IngredientModel(
        name='Борщ',
        measurement_unit='грамм',
    )
    db_session.add(ingredient)
    db_session.commit()
    db_session.refresh(ingredient)

    return ingredient


@fixture
def secondary_ingredient_object(db_session):
    """Второй объект ингредиента."""
    ingredient = IngredientModel(
        name='Курица',
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
    # for ing in ingredients:
    #     db_session.refresh(ing)

    return ingredients


@fixture
def ingredient_url():
    """Основной эндпоинт ингредиента."""
    return '/ingredients'


@fixture
def ingredient_detail_url(ingredient_object):
    """Эндпоинт конкретного ингредиента."""
    return f'/ingredients/{ingredient_object.id}'
