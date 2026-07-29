"""Модуль для тестирования эндпоинтов сущности Tag."""

import pytest
from fastapi import status
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize(
    'url',
    (
        lf('tag_url'),
        lf('tag_detail_url'),
    ),
)
def test_urls_tag(
    auth_client,
    url,
):
    """Тестирование эндпоинтов тега."""
    response = auth_client.get(url)
    assert (
        response.status_code == status.HTTP_200_OK
    ), f'Ошибка {response.json()}'
