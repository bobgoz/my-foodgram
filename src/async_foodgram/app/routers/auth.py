"""Модуль, содержащий роутеры для работы с токенами.
Эндпоинты:
    /auth/token/login/ -  Получения токена (авторизация).
    /auth/token/logout/ -  Удаление токена (выход из учетной записи).

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from async_foodgram.app.auth import create_access_token, get_current_user
from async_foodgram.app.db_depends import get_session
from async_foodgram.app.models import UserModel
from async_foodgram.app.schemas.auth import TokenResponseSchema
from async_foodgram.app.schemas.users import LoginSchema

router = APIRouter(
    prefix='/auth/token',
    tags=['auth'],
)


@router.post(
    '/login',
    response_model=TokenResponseSchema,
    summary='Вход пользователя',
    description='Аутентификация пользователя по email и паролю.'
    'Возвращает JWT токен.',
)
async def login(
    login_data: LoginSchema, session: Session = Depends(get_session)
) -> TokenResponseSchema:
    """Эндпоинт для входа пользователя."""
    user = session.scalar(
        select(UserModel).where(UserModel.email == login_data.email)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не зарегистрирован',
        )
    access_token = create_access_token(data={'sub': user.email})
    return TokenResponseSchema(auth_token=access_token)


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: UserModel = Depends(get_current_user)):
    """Эндпоинт для удаления токена (выхода из учетной записи)."""
    return None
