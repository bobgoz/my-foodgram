from http import HTTPStatus

from fastapi import status

from async_foodgram.app.schemas.users import (
    UserAfterRegistrationSchema,
    UserDetailSchema,
)


def test_registration_user(
    client,
    users_url,
    registration_form_data,
):
    """Тест регистрации пользователя."""
    response = client.post(users_url, json=registration_form_data)
    data = response.json()
    assert response.status_code == HTTPStatus.CREATED, f'{data}'
    expected_fields = set(UserAfterRegistrationSchema.model_fields)
    assert expected_fields.issubset(data.keys()), (
        f'Вывод не соответствует ожиданиям, {data}',
    )


def test_detail_url(
    auth_client,
    detail_user_endpoint,
):
    """Тестирование юрла детального отображения."""
    response = auth_client.get(detail_user_endpoint)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    fields = set(UserDetailSchema.model_fields)
    assert fields.issubset(data.keys()), (
        f'Вывод не соответствует ожиданиям, {data}',
    )


def test_user_profile(
    auth_client,
    me_url,
):
    """Тестирование юрла с профилем пользователя"""
    response = auth_client.get(me_url)
    data = response.json()
    assert response.status_code == HTTPStatus.OK, f'{data}'
    fields = set(UserDetailSchema.model_fields)
    assert fields.issubset(data.keys()), (
        f'Вывод не соответствует ожиданиям, {data}',
    )


def test_user_avatar_url(
    auth_client,
    avatar_endpoint,
):
    """Тестирование юрла с аватаром."""
    response = auth_client.get(avatar_endpoint)
    assert response.status_code == HTTPStatus.OK, f'{response.json()}'


def test_delete_avatar(
    auth_client,
    avatar_endpoint,
):
    """Тестирование  удаления  аватара."""
    response = auth_client.delete(avatar_endpoint)
    assert response.status_code == HTTPStatus.NO_CONTENT
