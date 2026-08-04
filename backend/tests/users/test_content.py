"""Модуль тестирования контента сущности user."""

from fastapi import status


def test_users_list(
    users_objects,
    auth_client,
    users_url,
):
    """
    Проверка, что выводится 10 пользователей в эндпоинте /users/.

    Примечание: Фикстура users_objects создает 9 объектов, но выводится 10,
    так как авторизованный клиент возвращает создает еще одного
    пользователя.
    """
    response = auth_client.get(users_url)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK, f'{data}'
    count = len(data['result'])
    assert (count) == 10, (
        f'Ожидалось 10 объектов, получено {count}. Детали: {data}',
    )
