"""Модуль для тестирования эндпоинтов сущности Recipe."""

from fastapi import status


def test_create_recipe(auth_client, recipe_create_form_data, recipe_url):
    """Тестирование создания рецепта."""
    response = auth_client.post(recipe_url, json=recipe_create_form_data)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f'Ошибка: {response.json()}'
