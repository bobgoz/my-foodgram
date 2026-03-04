from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db_depends import get_session
from src.models.users import UserModel
from src.schemas.users import (
    UserListSchema as UserSchema,
    UserCreate,
    UserDetailSchema,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def user_registration(
    user_create: UserCreate,
    session: Session = Depends(get_session),
):
    """Регистрация пользователя"""

    user = UserModel(**user_create.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get('/{user_id}', response_model=UserDetailSchema)
async def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
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
