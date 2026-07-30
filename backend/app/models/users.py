from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from backend.app.auth import hash_password
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
    recipes: Mapped[list['RecipeModel']] = relationship(
        back_populates='author'
    )

    @validates('password')
    def validate_password(self, key, value: str) -> str:
        """
        Валидатор пароля.
        Автоматически хеширует пароль.
        """
        if not value.startswith('$2b$'):
            value = hash_password(value)

        return value
