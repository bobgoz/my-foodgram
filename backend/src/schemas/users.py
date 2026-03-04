from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Базовая User схема"""

    email: EmailStr
    username: str = Field(title='Имя пользователя', pattern='^[\w.@+-]+\z')
    first_name: str
    last_name: str


class UserCreate(UserBase):
    """Схема для создания пользователя"""

    password: str


class UserListSchema(UserBase):
    """Схема для отображения списка пользователей"""

    id: int


class UserDetailSchema(UserListSchema):
    """Схема для отображения детальной информации о пользователе"""

    is_subscribed: bool
    avatar: str
