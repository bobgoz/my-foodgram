from sqlalchemy.orm import Mapped, mapped_column


class PrimaryKeyMixin:
    """Миксин с полем id для соответствующих моделей"""

    id: Mapped[int] = mapped_column(primary_key=True)
