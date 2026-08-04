"""Модуль для тестирования эндпоинтов /users/."""

import pytest
from fastapi import status
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize(
    ('url'),
    (
        lf('users_url'),
        lf('me_url'),
        lf('avatar_endpoint'),
        lf('set_password_endpoint'),
        lf('detail_user_endpoint'),
    ),
)
def test_anonim_client_not_allowed(client, url):
    """Проверка, что неавторизованному пользователю доступ запрещен."""
    response = client.get(url)
    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    ), f'Ожидался статус 401, получен {response.status_code}'
