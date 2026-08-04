"""Модуль для тестирования сервиса auth."""

from fastapi import status


def test_login_url(user, login_form_data, client, login_url):
    """Тест, проверяющий получение токена."""
    response = client.post(login_url, json=login_form_data)
    assert response.status_code == status.HTTP_200_OK


def test_logout_url(user, auth_client, logout_url):
    """Тест, проверяющий выход из системы."""
    response = auth_client.post(logout_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_anonim_client_not_allowed(client, logout_url):
    """Проверка, что неавторизованному пользователю доступ запрещен."""
    response = client.post(logout_url)
    assert (
        response.status_code == status.HTTP_401_UNAUTHORIZED
    ), f'Ожидался статус 401, получен {response.status_code}'
