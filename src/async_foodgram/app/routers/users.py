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

from async_foodgram.app.auth import get_current_user, verify_password
from async_foodgram.app.db_depends import get_session
from async_foodgram.app.models import UserModel
from async_foodgram.app.schemas.auth import TokenResponseSchema
from async_foodgram.app.schemas.users import (
    LoginSchema,
    SetPasswordSchema,
    UserAvatarSchema,
    UserCreate,
    UserDetailSchema,
)
from async_foodgram.app.schemas.users import UserListSchema as UserSchema

router = APIRouter(prefix='/users', tags=['users'])


T = TypeVar('T')

CustomPage = CustomizedPage[
    Page[T],
    UseFieldsAliases(
        items='result',
        total='count',
    ),
]


@router.post('/set_password', status_code=status.HTTP_204_NO_CONTENT)
async def set_password(
    set_password: SetPasswordSchema,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Назначение нового пароля."""

    if not verify_password(
        set_password.current_password, current_user.password
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail='Текущий пароль введён неправильно.',
        )

    current_user.password = set_password.new_password
    session.commit()
    return None


@router.post(
    '/',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def user_registration(
    user_create: UserCreate,
    session: Session = Depends(get_session),
) -> UserSchema:
    """Регистрация пользователя."""

    result = session.scalar(
        select(UserModel).where(UserModel.email == user_create.email),
    )
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Такой email уже занят',
        )

    user = UserModel(**user_create.model_dump())

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get(
    '/me',
    response_model=UserDetailSchema,
    summary='Получение профиля текущего пользователя',
)
async def get_user_profile(
    current_user: UserModel = Depends(get_current_user),
) -> UserDetailSchema:
    """Получение профиля пользователя."""
    return UserDetailSchema.model_validate(current_user)


@router.get('/me/avatar', response_model=UserAvatarSchema)
async def get_user_avatar(
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> UserAvatarSchema:
    """Получение аватара пользователя."""
    return UserAvatarSchema(avatar=current_user.avatar)


@router.put(
    '/me/avatar',
    status_code=status.HTTP_200_OK,
    response_model=UserAvatarSchema,
)
async def add_avatar(
    avatar_data: UserAvatarSchema,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> UserAvatarSchema:
    """Добавление аватара."""
    current_user.avatar = UserAvatarSchema.model_dump(**avatar_data)
    session.commit()
    session.refresh(current_user)
    return UserAvatarSchema


@router.delete('/me/avatar', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_avatar(
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Удаление аватара."""
    current_user.avatar = ""
    session.commit()
    return None


@router.get('/{user_id}', response_model=UserDetailSchema)
async def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> UserDetailSchema:
    """Получение пользователя по id."""
    user = session.scalar(
        select(UserModel).where(UserModel.id == user_id),
    )
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f'Пользователя с таким id {user_id} не найдено',
        )
    return user


@router.get('/', response_model=CustomPage[UserDetailSchema])
async def get_pagination_users(
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> CustomPage[UserDetailSchema]:
    """Получение пагинированного списка пользователей"""

    return paginate(session, select(UserModel).order_by(UserModel.id))
