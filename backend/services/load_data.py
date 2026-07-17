from sqlalchemy import delete

from app.database import SessionLocal
from app.models.tags import TagModel
from app.models.ingredients import IngredientModel
from app.models.users import UserModel

from app.auth.security import hash_password

TAG_DATA = [
    {
        'name': 'Суп',
        'slug': 'sup',
    },
    {
        'name': 'Завтрак',
        'slug': 'breakfast',
    },
    {
        'name': 'Ужин',
        'slug': 'Supper',
    },
    {
        'name': 'Обед',
        'slug': 'lunch',
    },
    {
        'name': 'Перекус',
        'slug': 'snack',
    },
]

INGREDIENT_DATA = [
    {
        'name': 'Морковка',
        'measurement_unit': 'шт',
    },
    {
        'name': 'Репчатый лук',
        'measurement_unit': 'шт',
    },
    {
        'name': 'Молоко',
        'measurement_unit': 'мл',
    },
    {
        'name': 'Черный перец',
        'measurement_unit': 'ч.ложка',
    },
    {
        'name': 'Филе курицы',
        'measurement_unit': 'грамм',
    },
]

USER_DATA = [
    {
        'email': f'vasua_{i}@mail.ru',
        'username': f'vasya_{i}',
        'first_name': 'Вася',
        'last_name': 'Василий',
        'password': hash_password('12345'),
    }
    for i in range(50)
]

# USER_DATA = [
#     {
#         'email': 'vasua@mail.ru',
#         'username': 'vasya',
#         'first_name': 'Вася',
#         'last_name': 'Василий',
#         'password': '12345',
#     },
#     {
#         'email': 'nikita@mail.ru',
#         'username': 'nikita',
#         'first_name': 'Никита',
#         'last_name': 'Пупкин',
#         'password': '12345',
#     },
#     {
#         'email': 'tema@mail.ru',
#         'username': 'tema',
#         'first_name': 'Артём',
#         'last_name': 'Ханов',
#         'password': '12345',
#     },
# ]


def load_data():
    """
    Загрузка данных в базу данных.
    Предварительное удаление записей
    избавляет от необходимости следить
    за целостностью данных в БД.
    """
    try:
        with SessionLocal.begin() as session:
            session.execute(delete(TagModel))
            session.execute(delete(IngredientModel))
            session.execute(delete(UserModel))

            session.bulk_insert_mappings(TagModel, TAG_DATA)
            session.bulk_insert_mappings(IngredientModel, INGREDIENT_DATA)
            session.bulk_insert_mappings(UserModel, USER_DATA)
        print('Успешно!')
    except Exception as e:
        print(f'Ошибка: {e}')


load_data()
