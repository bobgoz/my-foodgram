"""Модуль для тестирования сервиса auth."""

from fastapi import status


def test_login_url(user, login_form_data, client):
    """Тест, проверяющий получение токена."""
    login_url = '/auth/token/login'
    response = client.post(login_url, json=login_form_data)
    assert response.status_code == status.HTTP_200_OK


def test_login_url(user, auth_client):
    """Тест, проверяющий выход из системы."""
    login_url = '/auth/token/logout'
    response = auth_client.post(login_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
