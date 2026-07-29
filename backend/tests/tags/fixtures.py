"""Модуль содержащий фикстуры для сущности Tag."""

from pytest import fixture

from backend.app.models import TagModel


@fixture
def tag_object(db_session):
    """Создание объекта Тег."""
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
    """Создание 10 тегов."""
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
    """Основной эндпоинт тега."""
    return '/tags'


@fixture
def tag_detail_url(tag_object):
    """Эндпоинт конкретного тега."""
    return f'/tags/{tag_object.id}'
