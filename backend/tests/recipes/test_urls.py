"""Модуль для тестирования эндпоинтов сущности Recipe."""

import pytest
from fastapi import status
from pytest_lazy_fixtures import lf

from backend.app.schemas.recipes import RecipeCreateSchema


@pytest.mark.parametrize(('url'), ((lf('recipe_url'),)))
def test_recipe_urls(auth_client, url):
    """Тестирование эндпоинтов сущности Recipe."""
    response = auth_client.get(url)
    assert (
        response.status_code == status.HTTP_200_OK
    ), f'Ошибка  {response.json()}'


@pytest.mark.parametrize(
    ('url'),
    (
        lf('recipe_url'),
        # lf('recipe_detail_url'),
    ),
)
def test_anonim_client_not_allowed(client, url):
    """Проверка, что неавторизованному пользователю доступ запрещен."""
    response = client.get(url)
    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    ), f'Ожидался статус 401, получен {response.status_code}'
    

