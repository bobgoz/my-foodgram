"""Модуль для тестирования контента сущности Recipe."""

from fastapi import status
from sqlalchemy import select

from backend.app.models import RecipeModel, ShoppingCartModel
from backend.app.schemas.recipes import RecipeResponseSchema


def test_response_recipe(
    auth_client,
    db_session,
    recipe_create_form_data,
    recipe_url,
):
    """Тестирование создания рецепта."""
    response = auth_client.post(recipe_url, json=recipe_create_form_data)
    data = response.json()
    message = f'Ошибка: {data}'

    assert response.status_code == status.HTTP_201_CREATED, message
    assert db_session.scalars(
        select(RecipeModel).where(RecipeModel.id == data.get('id'))
    ).first(), message
    expected_fields = set(RecipeResponseSchema.model_fields)

    assert expected_fields.issubset(
        data.keys()
    ), f'Вывод не соответствует ожиданиям, {data}'


def test_add_recipe_in_shopping_cart(
    auth_client,
    shopping_cart_url,
    db_session,
    recipe_id,
    user,
):
    """Тестирование добавления рецептв в список покупок и удаление."""
    response = auth_client.post(shopping_cart_url)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), 'Не удалось добавить рецепт в список покупок'

    assert db_session.scalar(
        select(ShoppingCartModel).where(
            ShoppingCartModel.user_id == user.id,
            ShoppingCartModel.recipe_id == recipe_id,
        )
    ), 'Не найдено рецепта в списке покупок.'

    dupl_response = auth_client.post(shopping_cart_url)
    assert (
        dupl_response.status_code == status.HTTP_400_BAD_REQUEST
    ), 'Рецепт не должен добавляться повторно в список покупок.'

    delete_response = auth_client.delete(shopping_cart_url)

    assert (
        delete_response.status_code == status.HTTP_204_NO_CONTENT
    ), f'Ожидался статус 204, получен {delete_response.status_code}'

    assert not db_session.scalar(
        select(ShoppingCartModel).where(
            ShoppingCartModel.user_id == user.id,
            ShoppingCartModel.recipe_id == recipe_id,
        )
    ), 'Не удалось удалить объект из списка покупок.'
