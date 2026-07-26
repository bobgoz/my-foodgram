from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.database import Base, SessionLocal
from backend.app.db_depends import get_session
from backend.app.main import app

from .fixtures.ingredients import *
from .fixtures.tags import *
from .fixtures.users import *

SQLITE_DATABASE_URL = 'sqlite:///./test_db.db'

engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
)

Base.metadata.create_all(bind=engine)


@fixture(scope='function')
def db_session():
    """Тестовая сессия"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@fixture(scope="function")
def client(db_session):
    """Тестовый клиент."""

    def override_get_session():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client


@fixture
def auth_client(client, login_form_data):
    """Авторизованный тестовый клиент."""

    response = client.post('auth/token/login', json=login_form_data)
    token = response.json().get('auth_token')
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
