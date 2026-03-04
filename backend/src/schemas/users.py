from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """Схема для создания пользователя"""

    email: EmailStr
    username: str = Field(title='Имя пользователя', pattern='^[\w.@+-]+\z')
    first_name: str
    last_name: str
    password: str


class UserListSchema(BaseModel):
    """Схема для отображения списка пользователей"""

    email: EmailStr
    id: int
    username: str
    first_name: str
    last_name: str


class UserDetailSchema(BaseModel):
    """Схема для отображения детальной информации о пользователе"""

    email: EmailStr
    id: int
    username: str
    first_name: str
    last_name: str
    is_subscribed: bool
    avatar: str
