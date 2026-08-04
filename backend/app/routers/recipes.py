from typing import Sequence

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import (
    delete,
    insert,
    select,
    update,
)
from sqlalchemy.orm import Session

from backend.app.auth import get_current_user
from backend.app.db_depends import get_session
from backend.app.models import (
    IngredientModel,
    RecipeModel,
    ShoppingCartModel,
    TagModel,
    UserModel,
)
from backend.app.models.associations import (
    recipe_ingredient,
    recipe_tag,
)
from backend.app.schemas.recipes import (
    IngredientInRecipeCreateSchema,
    RecipeCreateSchema,
    RecipeResponseSchema,
    ShoppingCartResponseSchema,
)

router = APIRouter(prefix='/recipes', tags=['recipes'])


def message_not_found(recipe_id) -> str:
    """Сообщение, если рецепт не найден."""
    return f'Рецепта с id: {recipe_id} не найдено.'


def message_forbidden() -> str:
    """Сообщение, если прав недостаточно."""
    return 'У вас недостаточно прав для выполнения данного действия.'


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

    recipe = RecipeModel(
        **recipe_create.model_dump(
            exclude={'ingredients', 'tags'},
        ),
        author_id=current_user.id,
    )

    session.add(recipe)
    session.commit()
    session.refresh(recipe)

    for ing in recipe_create.ingredients:
        stmt = insert(recipe_ingredient).values(
            recipe_id=recipe.id,
            ingredient_id=ing.id,
            amount=ing.amount,
        )
        session.execute(stmt)

    tags = session.scalars(
        select(TagModel).where(TagModel.id.in_(recipe_create.tags)),
    ).all()
    for tag in tags:
        recipe.tags.append(tag)

    session.commit()
    session.refresh(recipe)

    return recipe


@router.get(
    '/',
    response_model=list[RecipeResponseSchema],
    summary='Получение списка рецептов',
)
async def recipe_list(
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> list[RecipeResponseSchema]:
    """Возвращает список рецептов."""
    return session.scalars(select(RecipeModel)).all()


@router.get(
    '/{recipe_id}',
    response_model=RecipeResponseSchema,
    summary='Получение рецепта по id',
)
async def recipe_detail(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Получение рецепта по id."""
    recipe = session.get(RecipeModel, recipe_id)
    if not recipe:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            message_not_found(recipe_id),
        )

    return session.scalar(
        select(RecipeModel).where(RecipeModel.id == recipe_id),
    )


@router.put(
    '/{recipe_id}',
    response_model=RecipeResponseSchema,
    summary='Обновление рецепта.',
)
async def recipe_update(
    recipe_id: int,
    recipe_update: RecipeCreateSchema,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Обновление рецепта."""

    recipe = session.get(RecipeModel, recipe_id)
    if not recipe:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            message_not_found(recipe_id),
        )

    if recipe.author_id != current_user.id:
        raise HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE,
            message_forbidden(),
        )
    update_data = recipe_update.model_dump(exclude=('ingredients', 'tags'))
    session.execute(
        update(RecipeModel)
        .where(RecipeModel.id == recipe_id)
        .values(**update_data)
    )

    # Обновление ингредиентов.
    try:
        session.execute(
            delete(recipe_ingredient).where(
                recipe_ingredient.c.recipe_id == recipe_id
            )
        )
        for ing in recipe_update.ingredients:
            ingredient = session.get(IngredientModel, ing.id)
            if not ingredient:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f'Ингредиента с таким id: {ing.id} не существует.',
                )
            session.execute(
                insert(recipe_ingredient).values(
                    recipe_id=recipe_id,
                    ingredient_id=ing.id,
                    amount=ing.amount,
                )
            )
    except Exception as error:
        session.rollback()
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f'Ошибка при обновлении ингредиентов: {error}',
        )

    # Обновление тегов.
    try:
        session.execute(
            delete(recipe_tag).where(recipe_tag.c.recipe_id == recipe_id)
        )
        for tag_id in recipe_update.tags:
            tag = session.get(TagModel, tag_id)
            if not tag:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f'Тега с таким id: {tag_id} не существует.',
                )
            session.execute(
                insert(recipe_tag).values(
                    recipe_id=recipe_id,
                    tag_id=tag_id,
                )
            )

    except Exception as error:
        session.rollback()
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f'Ошибка при обновлении ингредиентов: {error}',
        )

    # Для тестирования.
    # for key, value in update_data.items():
    #     setattr(recipe, key, value)

    session.commit()
    session.refresh(recipe)

    return recipe


@router.delete('/{recipe_id}', status_code=status.HTTP_204_NO_CONTENT)
async def recipe_delete(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Удаление рецепта."""
    recipe = session.get(RecipeModel, recipe_id)
    if not recipe:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            message_not_found(recipe_id),
        )
    if recipe.author_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            message_forbidden(),
        )
    session.delete(recipe)
    session.commit()
    return None


@router.get('/{recipe_id}/get-link')
async def get_short_link(
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Получение короткой ссылки на рецепт."""
    return None


@router.get('/download_shopping_cart')
async def download_shopping_cart(
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
):
    """Скачать список покупок."""
    return None


@router.post(
    '/{recipe_id}/shopping_cart',
    status_code=status.HTTP_201_CREATED,
    response_model=ShoppingCartResponseSchema,
)
async def add_recipe_in_shopping_cart(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> ShoppingCartResponseSchema:
    """Добавление рецепта в список покупок."""
    recipe = session.get(RecipeModel, recipe_id)
    if not recipe:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            message_not_found(recipe_id),
        )

    existing = session.scalar(
        select(ShoppingCartModel).where(
            ShoppingCartModel.user_id == current_user.id,
            ShoppingCartModel.recipe_id == recipe_id,
        )
    )
    if existing:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Рецепт уже в списке покупок.',
        )
    cart_item = ShoppingCartModel(
        user_id=current_user.id,
        recipe_id=recipe_id,
    )
    session.add(cart_item)
    session.commit()
    session.refresh(cart_item)

    return cart_item


@router.delete(
    '/{recipe_id}/shopping_cart',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_recipe_from_shopping_cart(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    """Удаление рецепта из списка покупок."""
    recipe = session.get(RecipeModel, recipe_id)
    if not recipe:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            message_not_found(recipe_id),
        )
    cart_item = session.scalar(
        select(ShoppingCartModel).where(
            ShoppingCartModel.user_id == current_user.id,
            ShoppingCartModel.recipe_id == recipe_id,
        )
    )
    if not cart_item:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Рецепт не найден в списке покупок.',
        )

    session.delete(cart_item)
    session.commit()

    return None
