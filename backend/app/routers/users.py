from typing import TypeVar

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.customization import (
    CustomizedPage,
    UseExcludedFields,
    UseFieldsAliases,
    UseIncludeTotal,
    UseParamsFields,
)
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db_depends import get_session
from backend.app.models.users import UserModel
from backend.app.schemas.users import (
    SetPasswordSchema,
    UserAvatarSchema,
    UserCreate,
    UserDetailSchema,
)
from backend.app.schemas.users import UserListSchema as UserSchema

router = APIRouter(prefix='/users', tags=['users'])


T = TypeVar('T')

CustomPage = CustomizedPage[
    Page[T],
    UseFieldsAliases(
        items='result',
        total='count',
    ),
]


@router.post(
    '/',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def user_registration(
    user_create: UserCreate,
    session: Session = Depends(get_session),
) -> UserSchema:
    """Регистрация пользователя"""

    user = UserModel(**user_create.model_dump(exclude=['password']))
    user.set_password(user_create.password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get('/{user_id}', response_model=UserDetailSchema)
async def get_user_by_id(
    user_id: int, session: Session = Depends(get_session)
) -> UserDetailSchema:
    """Получение пользователя по id"""
    user = session.scalar(
        select(UserModel).where(UserModel.id == user_id),
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f'Пользователя с таким id {user_id} не найдено',
        )
    return user


@router.get('/users/me', response_model=UserDetailSchema)
async def get_user_profile(
    session: Session = Depends(get_session),
) -> UserDetailSchema:
    """Получение профиля пользователя."""
    # Имеет смысл реализовать после реализации аутентификации.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail='Эндпоинт не  реализован',
    )


@router.get('/users/me/avatar', response_model=UserAvatarSchema)
async def get_user_avatar(session: Session = Depends(get_session)):
    """Получение аватара пользователя."""
    # Имеет смысл реализовать после реализации аутентификации.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail='Эндпоинт не  реализован',
    )


@router.delete('/users/me/avatar', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_avatar(session: Session = Depends(get_session)):
    """Удаление аватара."""
    # Имеет смысл реализовать после реализации аутентификации.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail='Эндпоинт не  реализован',
    )


@router.post('/users/set_password')
async def set_password(
    set_password: SetPasswordSchema,
    session: Session = Depends(get_session),
):
    """Назначение нового пароля."""
    pass


@router.get('/', response_model=CustomPage[UserDetailSchema])
async def get_pagination_users(
    session: Session = Depends(get_session),
) -> CustomPage[UserDetailSchema]:
    """Получение пагинированного списка пользователей"""

    return paginate(session, select(UserModel).order_by(UserModel.id))
