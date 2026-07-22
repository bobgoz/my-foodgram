from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db_depends import get_session
from backend.app.models import IngredientModel
from backend.app.schemas.ingredients import IngredientSchema

router = APIRouter(prefix='/ingredients', tags=['ingredients'])


@router.get('/', response_model=list[IngredientSchema])
async def get_all_ingredients(
    session: Session = Depends(get_session),
) -> list['IngredientModel']:
    """Получение всех ингредиентов"""
    ingredients = session.scalars(select(IngredientModel)).all()
    return list(ingredients)


@router.get('/{ingredient_id}', response_model=IngredientSchema)
async def get_ingredient_by_id(
    ingredient_id: int, session: Session = Depends(get_session)
):
    """Получение ингредиента по id"""
    ingredient = session.scalar(
        select(IngredientModel).where(
            IngredientModel.id == ingredient_id,
        )
    )
    if not ingredient:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f'Ингредиента с id: {ingredient_id} не найдено.',
        )
    return ingredient
