from pydantic import BaseModel, Field, HttpUrl, model_validator

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


# class IngredientInRecipeResponseSchema(IngredientInRecipeCreateSchema):
class IngredientInRecipeResponseSchema(BaseModel):
    """Схема Ингредиент в рецепте в ответе на создание рецепта."""

    name: str
    measurement_unit: str
    amount: int = Field(
        description='Количество ингредиента',
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

    @model_validator(mode='before')
    @classmethod
    def build_ingredients(cls, data):
        """Преобразует recipe_ingredients в ingredients."""
        # Если data — это объект модели SQLAlchemy
        if hasattr(data, 'recipe_ingredients'):
            ingredients = []
            for recipe_ing in data.recipe_ingredients:
                ingredients.append(
                    {
                        'id': recipe_ing.ingredient.id,
                        'name': recipe_ing.ingredient.name,
                        'measurement_unit': recipe_ing.ingredient.measurement_unit,
                        'amount': recipe_ing.amount,  # ← Вот он, amount!
                    }
                )
            # Устанавливаем ingredients как атрибут объекта
            data.ingredients = ingredients
        return data

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
