"""Модуль  для тестирования логики сущности user."""

from fastapi import status

from backend.app.auth import verify_password


def test_hash_password(user, user_data):
    """Тестирование логики валидации и хеширования пароля."""
    assert user.password != user_data.get('password'), 'Пароль не хеширован.'
    assert user.password.startswith('$2b$'), 'Пароль не хеширован.'

    assert (
        verify_password(user_data['password'], user.password) is True
    ), 'Пароль не прошел верификацию.'


def test_set_password(
    auth_client,
    new_password_form_data,
    user_data,
    set_password_endpoint,
):
    """Тестирование назначения пароля."""
    response = auth_client.post(
        set_password_endpoint, json=new_password_form_data
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверка, если текущий пароль введен неправильно
    new_password_form_data['current_password'] = '4321'
    response = auth_client.post(
        set_password_endpoint, json=new_password_form_data
    )
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), f'{response.json()}'

    # Проверка, что пароли не совпадают.
    new_password_form_data['new_password'] = user_data['password']
    response = auth_client.post(
        set_password_endpoint,
        json=new_password_form_data,
    )
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), f'{response.json()}'
