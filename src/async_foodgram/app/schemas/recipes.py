from pydantic import BaseModel, Field, HttpUrl

from .tags import TagSchema
from .users import UserDetailSchema


class IngredientInRecipeCreateSchema(BaseModel):
    """Схема Ингредиент в рецепте при создании рецепта."""

    id: int
    amount: int


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


class IngredientInRecipeResponseSchema(IngredientInRecipeCreateSchema):
    """Схема Ингредиент в рецепте в ответе на создание рецепта."""

    name: str
    measurement_unit: str
    amount: int = Field(
        description='Количество ингредиента',
        default='Это временное решение',
    )

    class Config:
        from_attributes = True


class RecipeResponseSchema(BaseModel):
    """Схема для ответа после создания рецепта."""

    id: int
    tags: list[TagSchema]
    author: UserDetailSchema
    ingredients: list[IngredientInRecipeResponseSchema]
    is_favorited: bool = Field(default=False)
    is_in_shopping_cart: bool = Field(default=False)
    name: str
    # image: HttpUrl
    image: str
    text: str
    cooking_time: int

    class Config:
        from_attributes = True


class ShoppingCartResponseSchema(BaseModel):
    """Схема для ответа при добавлении рецепта в список покупок."""

    id: int
    name: str = Field(default='Это временное решение')
    # image: HttpUrl
    image: str = Field(default='Это временное решение')
    cooking_time: int = Field(default=100000)

    class Config:
        from_attributes = True
