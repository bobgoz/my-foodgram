from factory.alchemy import SQLAlchemyModelFactory
from pytest_factoryboy import register

from .app.models.tags import TagModel


@register
class FactoryTag(SQLAlchemyModelFactory):
    """Фабрика  для модели Tag"""

    class Meta:
        model = TagModel
