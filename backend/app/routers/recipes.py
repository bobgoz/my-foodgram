from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.auth import get_current_user
from backend.app.db_depends import get_session
from backend.app.models import (
    IngredientModel,
    RecipeModel,
    TagModel,
    UserModel,
)
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
    current_user: UserModel = Depends(get_current_user),
) -> RecipeResponseSchema:
    """Эндпоинт для создания рецепта."""

    ingredient_idx = [ing.id for ing in recipe_create.ingredients]
    tag_idx = recipe_create.tags
    recipe = RecipeModel(
        **recipe_create.model_dump(
            exclude={'ingredients', 'tags'},
        ),
        author_id=current_user.id,
    )
    ingredients = session.scalars(
        select(IngredientModel).where(IngredientModel.id.in_(ingredient_idx))
    ).all()
    tags = session.scalars(
        select(TagModel).where(TagModel.id.in_(tag_idx))
    ).all()

    for ing in ingredients:
        recipe.ingredients.append(ing)

    for tag in tags:
        recipe.tags.append(tag)

    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe
