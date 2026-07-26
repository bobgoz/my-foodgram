from pytest import fixture

from backend.app.models.users import UserModel


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
def users(db_session):
    """Создание 10 пользователей."""
    users = [user for i in range(10)]
    db_session.add_all(users)
    db_session.commit()


@fixture(scope='function')
def registration_form_data():
    """Данные для регистрации"""
    return dict(
        email='test@mail.ru',
        username='test',
        first_name='test',
        last_name='test',
        password="SecurePass123!",
    )


@fixture
def login_form_data(registration_form_data):
    """Данные для логирования пользователя."""
    email = registration_form_data.get('email')
    password = registration_form_data.get('password')
    return dict(
        email=email,
        password=password,
    )
