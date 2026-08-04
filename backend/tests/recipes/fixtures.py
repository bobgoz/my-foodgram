"""Модуль с фикстурами для сущности Recipe."""

from pytest import fixture
from sqlalchemy import delete, insert, select

from backend.app.models import RecipeModel
from backend.app.models.associations import recipe_ingredient, recipe_tag
from backend.app.schemas.recipes import RecipeCreateSchema


@fixture
def recipe_url():
    """Основной эндпоинт рецепта."""
    return '/recipes'


@fixture
def recipe_detail_url(recipe_object):
    """Эндпоинт с детальным отображением рецепта."""
    return f'/recipes/{recipe_object.id}'


@fixture
def shopping_cart_url(recipe_object):
    """Эндпоинт для добавления рецепта с список покупок."""
    return f'/recipes/{recipe_object.id}/shopping_cart'


@fixture
def recipe_create_form_data(ingredient_object, tag_object):
    """Форма для создания рецепта."""
    return dict(
        ingredients=[
            dict(
                id=ingredient_object.id,
                amount=30,
            ),
        ],
        tags=[
            tag_object.id,
        ],
        image="image",
        name="Борщ",
        text="Вкусный борщ",
        cooking_time=60,
    )


@fixture
def recipe_id(recipe_object):
    """Возвращает ID созданного рецепта."""
    return recipe_object.id


@fixture
def recipe_object(
    recipe_create_form_data,
    user,
    auth_client,
    tag_object,
    ingredient_object,
    db_session,
):
    """Объект рецепта."""
    schema = RecipeCreateSchema(**recipe_create_form_data)
    recipe_data = schema.model_dump(exclude={'ingredients', 'tags'})
    recipe = RecipeModel(**recipe_data, author_id=user.id)
    ingredients = recipe_create_form_data['ingredients']
    db_session.add(recipe)
    db_session.flush()

    print(ingredients)
    for ing_data in recipe_create_form_data['ingredients']:
        db_session.execute(
            insert(recipe_ingredient).values(
                recipe_id=recipe.id,
                ingredient_id=ing_data['id'],
                amount=ing_data['amount'],
            )
        )

    for tag_data in recipe_create_form_data['tags']:
        db_session.execute(
            insert(recipe_tag).values(
                recipe_id=recipe.id,
                tag_id=tag_data,
            )
        )
    db_session.commit()
    db_session.refresh(recipe)
    return recipe


@fixture
def recipe_update_form_data(
    secondary_tag_object,
    secondary_ingredient_object,
):
    """Форма обновления рецепта."""
    return dict(
        ingredients=[
            dict(
                id=secondary_ingredient_object.id,
                amount=400,
            )
        ],
        tags=[
            secondary_tag_object.id,
        ],
        image="image_2",
        name="Запеканка",
        text="Вкуснятина",
        cooking_time=60,
    )
