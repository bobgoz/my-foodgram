from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from backend.app.db_depends import get_session
from backend.app.models import RecipeModel
from backend.app.schemas.recipes import (
    RecipeCreateSchema,
    RecipeResponseSchema,
)

router = APIRouter(prefix='/recipes', tags=['recipes'])


@router.post(
    '/',
    response_model=RecipeResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Создание рецепта.',
)
async def create_recipe(
    recipe_create: RecipeCreateSchema,
    session: Session = Depends(get_session),
) -> RecipeResponseSchema:
    """Эндпоинт  для создания рецепта."""
    recipe = RecipeModel(**recipe_create.model_dump())
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe
