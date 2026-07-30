"""Модуль для тестирования контента сущности Recipe."""

from fastapi import status
from sqlalchemy import select

from backend.app.models import RecipeModel
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
