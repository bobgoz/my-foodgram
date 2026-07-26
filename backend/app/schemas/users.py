from pydantic import BaseModel, EmailStr, Field


class UserEmail(BaseModel):
    """Схема, содержащая поле email."""

    email: EmailStr


class UserBase(UserEmail):
    """Базовая User схема."""

    username: str = Field(title='Имя пользователя', pattern='^[\\w.@+-]+\\z')
    first_name: str
    last_name: str


class UserCreate(UserBase):
    """Схема для создания пользователя."""

    password: str


class UserLoginSchema(BaseModel):
    """Схема для входа пользователя."""

    email: EmailStr
    password: str


class UserListSchema(UserBase):
    """Схема для отображения списка пользователей."""

    id: int


class BaseAvatarSchema(BaseModel):
    """Базовая схема с аватаром."""

    avatar: str


class UserDetailSchema(UserListSchema, BaseAvatarSchema):
    """Схема для отображения детальной информации о пользователе."""

    is_subscribed: bool


class UserAfterRegistrationSchema(UserListSchema):
    """Схема для отображения информации после регистрации пользователя."""

    pass


class UserAvatarSchema(BaseAvatarSchema):
    """Схема для аватара пользователя."""

    pass


class SetPasswordSchema(BaseModel):
    """Схема для назначения нового пароля."""

    new_password: str = Field(title='Новый пароль', min_length=8)
    current_password: str = Field(title='Текущий пароль')
