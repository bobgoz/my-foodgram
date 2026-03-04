from pydantic import BaseModel, Field


class IngredientSchema(BaseModel):
    """Схема для отображения ингредиентов"""

    id: int
    name: str
    measurement_unit: str = Field(description='Единица измерения')
