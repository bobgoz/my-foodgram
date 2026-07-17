from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.database import Base, SessionLocal
from backend.app.db_depends import get_session
from backend.app.main import app
from backend.app.models.tags import TagModel

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
def tag_object(db_session):
    tag = TagModel(
        name='Борщ',
        slug='borsch',
    )
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)

    return tag


@fixture
def tags(db_session):
    """Создание 10 тегов"""
    tags = [
        TagModel(
            name=f'Завтрак_{i}',
            slug=f'breakfast_{i}',
        )
        for i in range(10)
    ]
    db_session.add_all(tags)
    db_session.commit()


@fixture
def tag_url():
    return '/tags'


@fixture
def tag_detail_url(tag_object):
    return f'/tags/{tag_object.id}'


@fixture
def tag_form():
    return dict(
        tag='Молочные продукты',
        slug='milk',
    )


@fixture
def create_tag_url():
    return ''
