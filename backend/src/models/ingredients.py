from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


from src.models.constants import MAX_LENGTH_NAME, MAX_LENGTH_MEASUREMENT_UNIT
from src.models.mixins import PrimaryKeyMixin


class IngredientModel(Base, PrimaryKeyMixin):
    """Модель Ингредиента"""

    __tablename__ = 'ingredients'
    name: Mapped[str] = mapped_column(String(MAX_LENGTH_NAME), nullable=False)
    measurement_unit: Mapped[str] = mapped_column(
        String(MAX_LENGTH_MEASUREMENT_UNIT),
        nullable=False,
    )
