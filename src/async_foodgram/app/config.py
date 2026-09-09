import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

is_env_file = load_dotenv(BASE_DIR / '.env')
if not is_env_file:
    raise RuntimeError(
        'Не найдено файла с переменной окружения. '
        'Стоит проверить существование файла переменной окружения '
        f'по пути {BASE_DIR}',
    )


class Settings:
    """Конфигурация с переменными окружения."""

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError(
            'Переменная SECRET_KEY не задана в переменных окружения!',
        )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10000
    ALGORITHM: str = 'HS256'
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/foodgram",
    )
    if not DATABASE_URL:
        raise RuntimeError(
            'Переменная DATABASE_URL не задана в переменных окружения!',
        )
    DEBUG = os.getenv('DEBUG', 'true') == 'true'


settings = Settings()
