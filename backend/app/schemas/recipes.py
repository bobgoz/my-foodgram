from pydantic import BaseModel, Field, HttpUrl

from .tags import TagSchema
from .users import UserDetailSchema


class IngredientInRecipeCreateSchema(BaseModel):
    """Схема Ингредиент в рецепте при создании рецепта."""

    id: int
    amount: int


class IngredientInRecipeResponseSchema(IngredientInRecipeCreateSchema):
    """Схема Ингредиент в рецепте в ответе на создание рецепта."""

    name: str
    measurement_unit: str


class RecipeCreateSchema(BaseModel):
    """Схема для создания рецепта."""

    ingredients: list[IngredientInRecipeCreateSchema] = Field(
        description='Список ингредиентов',
    )
    tags: list[int] = Field(description='Список Id тегов')
    image: str
    name: str
    text: str
    cooking_time: int


class RecipeResponseSchema(BaseModel):
    """Схема для ответа после создания рецепта."""

    id: int
    tags: list[TagSchema]
    author: UserDetailSchema
    ingredients: list[IngredientInRecipeResponseSchema]
    is_favorited: bool
    is_in_shopping_cart: bool
    name: str
    image: HttpUrl
    text: str
    cooking_time: int
