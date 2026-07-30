"""Модуль с фикстурами для сущности Recipe."""

from pytest import fixture


@fixture
def recipe_url():
    """Основной эндпоинт рецепта."""
    return '/recipes'


@fixture
def recipe_create_form_data():
    """Форма для создания рецепта."""
    return dict(
        ingredients=[
            {
                "id": 0,
                "amount": 10,
            }
        ],
        tags=[
            1,
        ],
        image="image",
        name="Борщ",
        text="Вкусный борщ",
        cooking_time=60,
    )


#     )
# {
#   "ingredients": [
#     {
#       "id": 0,
#       "amount": 0
#     }
#   ],
#   "tags": [
#     0
#   ],
#   "image": "string",
#   "name": "string",
#   "text": "string",
#   "cooking_time": 0
# }
