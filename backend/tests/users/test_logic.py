"""Модуль  для тестирования логики сущности user."""

from backend.app.auth import verify_password


def test_hash_password(user, user_data):
    """Тестирование логики валидации и хеширования пароля."""
    assert user.password != user_data.get('password'), 'Пароль не хеширован.'
    assert user.password.startswith('$2b$'), 'Пароль не хеширован.'

    assert (
        verify_password(user_data['password'], user.password) is True
    ), 'Пароль не прошел верификацию.'
