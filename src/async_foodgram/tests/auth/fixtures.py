"""Модуль с фикстурами для логики аутентификации."""

from pytest import fixture


@fixture
def logout_url():
    """Эндпоинт для входа."""
    return '/auth/token/logout'


@fixture
def login_url():
    """Эндпоинт для выхода."""
    return '/auth/token/login'
