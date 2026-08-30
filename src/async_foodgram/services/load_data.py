import csv

from sqlalchemy import delete

from async_foodgram.app.database import SessionLocal
from async_foodgram.app.models import IngredientModel, TagModel, UserModel


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

            with open('tags.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                tags = []
                for row in reader:
                    name = row.get('name')
                    slug = row.get('slug')
                    tags.append(dict(name=name, slug=slug))

            session.bulk_insert_mappings(TagModel, tags)

            with open('ingredients.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                ingredients = []
                for row in reader:
                    name = row.get('name')
                    meas = row.get('meas')
                    ingredients.append(dict(name=name, meas=meas))

            session.bulk_insert_mappings(IngredientModel, ingredients)

            # session.bulk_insert_mappings(UserModel, USER_DATA)
        print('Успешно!')
    except Exception as e:
        print(f'Ошибка: {e}')


load_data()
