from http import HTTPStatus

from backend.app.schemas.users import (
    UserAfterRegistrationSchema,
    UserDetailSchema,
)


def test_registration_user(client, user_registration_form_data):
    """Тест регистрации пользователя."""
    response = client.post('/users', json=user_registration_form_data)
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED, f'{data}'
    expected_fields = set(UserAfterRegistrationSchema.model_fields)
    assert expected_fields.issubset(data.keys()), (
        f'Вывод не соответствует ожиданиям, {data}',
    )


def test_detail_url(client, user):
    """Тестирование юрла детального отображения."""
    url = f'/users/{user.id}'
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    fields = set(UserDetailSchema.model_fields)
    assert fields.issubset(data.keys()), (
        f'Вывод не соответствует ожиданиям, {data}',
    )


def test_user_profile(client, user):
    """Тестирование юрла с профилем пользователя"""
    url = '/users/me'
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    fields = set(UserDetailSchema.model_fields)
    assert fields.issubset(data.keys()), (
        f'Вывод не соответствует ожиданиям, {data}',
    )


def test_user_avatar_url(client):
    """Тестирование брла с аватаром."""
    url = '/users/me/avatar'
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_delete_avatar(client):
    """Тестирование  удаления  аватара."""
    url = '/users/me/avatar'
    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_url_set_password(client):
    """Тестирование назначения пароля."""
    url = '/users/set_password''
    response = client.delete(url)
    assert response.status_code == HTTPStatus.NO_CONTENT

def test_auth():
    """ Тест, связанный с аутентификацией """
    pass
    
def test_auth_2():
    """ Тест, связанный с аутентификацией """
    pass
