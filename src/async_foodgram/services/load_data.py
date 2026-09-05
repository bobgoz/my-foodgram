import csv
from pathlib import Path

from sqlalchemy import delete

from async_foodgram.app.database import SessionLocal
from async_foodgram.app.models import IngredientModel, TagModel, UserModel

BASE_DIR = Path(__file__).parent

TAGS_PATH = BASE_DIR / 'tags.csv'
INGREDIENTS_PATH = BASE_DIR / 'ingredients.csv'


def load_data():
    """
    Загрузка данных в базу данных.
    Предварительное удаление записей
    избавляет от необходимости следить
    за целостностью данных в БД.
    """
    with SessionLocal.begin() as session:
        session.execute(delete(TagModel))
        session.execute(delete(IngredientModel))
        session.execute(delete(UserModel))

        with open(TAGS_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            tags = []
            for row in reader:
                name = row.get('name')
                slug = row.get('slug')
                tags.append(dict(name=name, slug=slug))

        session.bulk_insert_mappings(TagModel, tags)
        print(f'Успешно создано {len(tags)} тегов.')

        with open(INGREDIENTS_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            ingredients = []
            for row in reader:
                name = row['name'].strip()
                measurement_unit = row['meas'].strip()
                ingredients.append(
                    dict(name=name, measurement_unit=measurement_unit)
                )

        session.bulk_insert_mappings(IngredientModel, ingredients)
        print(f'Успешно создано {len(ingredients)} ингредиентов.')

        # session.bulk_insert_mappings(UserModel, USER_DATA)


load_data()
