from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.auth.security import hash_password
from backend.app.database import Base
from backend.app.models.mixins import PrimaryKeyMixin

MAX_LENGTH_EMAIL_FIELD = 254
MAX_LENGTH_USERNAME_FIELD = 150


class UserModel(PrimaryKeyMixin, Base):
    """Модель пользователя"""

    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(
        String(MAX_LENGTH_EMAIL_FIELD),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(MAX_LENGTH_USERNAME_FIELD),
        nullable=False,
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_USERNAME_FIELD),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_USERNAME_FIELD),
        nullable=False,
    )
    is_subscribed: Mapped[bool] = mapped_column(default=False)
    avatar: Mapped[str] = mapped_column(default='')
    password: Mapped[str] = mapped_column(String(50))

    def set_password(self, password: str):
        """Установка хешированного пароля"""
        self.password = hash_password(password)
