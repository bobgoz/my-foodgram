"""Модуль для тестирования эндпоинтов /ingredients/."""

import pytest
from fastapi import status
from pytest_lazy_fixtures import lf


def test_ingredient_url(
    ingredient_url,
    client,
):
    response = client.get(ingredient_url)
    assert response.status_code == 200, f'{response.json()}'


def test_get_ingredient_by_id(
    ingredient_detail_url, ingredient_object, client
):
    response = client.get(ingredient_detail_url)
    assert response.status_code == 200, f'{response.json()}'


@pytest.mark.parametrize(
    ('url'),
    (
        lf('tag_url'),
        lf('tag_detail_url'),
    ),
)
def test_anonim_client_not_allowed(client, url):
    """Проверка, что неавторизованному пользователю доступ запрещен."""
    response = client.get(url)
    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    ), f'Ожидался статус 401, получен {response.status_code}'
