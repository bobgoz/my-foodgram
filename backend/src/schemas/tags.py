from pydantic import BaseModel


class TagSchema(BaseModel):
    """Схема для отображения тега"""

    id: int
    name: str
    slug: str
