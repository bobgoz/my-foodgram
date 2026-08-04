"""Модуль с фикстурами для сущности users."""

from pytest import fixture

from backend.app.models import UserModel


@fixture
def user_data() -> dict:
    return dict(
        email='test@mail.ru',
        username='test_user',
        first_name='test',
        last_name='test',
        password='password',
    )


@fixture
def user(db_session, user_data):
    """Пользователь."""
    user = UserModel(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@fixture
def users_objects(db_session, user_data):
    """Создание 9 разных пользователей."""
    USERS_COUNT = 9
    users = []
    for i in range(USERS_COUNT):
        user = UserModel(
            email=f'test_{i}@mail.ru',
            username=f'test_user_{i}',
            first_name=f'First_{i}',
            last_name=f'Last_{i}',
            password='SecurePass123!',
        )
        users.append(user)

    db_session.add_all(users)
    db_session.commit()

    for user in users:
        db_session.refresh(user)

    return users


@fixture(scope='function')
def registration_form_data(user_data):
    """Данные для регистрации."""
    return user_data


@fixture
def login_form_data(registration_form_data):
    """Данные для входа пользователя."""
    email = registration_form_data.get('email')
    password = registration_form_data.get('password')
    return dict(
        email=email,
        password=password,
    )


@fixture
def new_password_form_data(user_data) -> dict:
    """Форма с новым паролем."""
    return dict(
        new_password='new_password',
        current_password=user_data['password'],
    )


@fixture
def users_url():
    """Эндпоинт /users."""
    return '/users'


@fixture
def me_url():
    """Эндпоинт /users/me."""
    return '/users/me'


@fixture
def avatar_endpoint():
    """Эндпоинт /users/me/avatar."""
    return '/users/me/avatar'


@fixture
def set_password_endpoint():
    """Эндпоинт /users/set_password."""
    return '/users/set_password'


@fixture
def detail_user_endpoint(user):
    """Эндпоинт /users/{user_id}."""
    return f'/users/{user.id}'
