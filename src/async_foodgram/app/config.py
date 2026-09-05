import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError(
        'Переменная SECRET_KEY не задана в переменных окружения!',
    )

ALGORITHM = os.getenv('ALGORITHM', 'HS256')
