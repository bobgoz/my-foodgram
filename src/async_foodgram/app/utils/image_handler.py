"""Утилиты для работы с изображениями рецептов."""

import base64
import uuid
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile, status

from async_foodgram.app.config import BASE_DIR


class ImageHandler:
    """Обработчик изображений для рецептов."""

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    UPLOAD_DIR = BASE_DIR / 'media' / 'recipes'

    @classmethod
    def setup_upload_dir(cls) -> None:
        """Создать директорию для загрузки, если её нет."""
        cls.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate_image_extension(cls, filename: str) -> bool:
        """Проверить расширение файла."""
        ext = Path(filename).suffix.lower()
        return ext in cls.ALLOWED_EXTENSIONS

    @classmethod
    async def save_upload_file(cls, file: UploadFile) -> str:
        """
        Сохранить загруженный файл.

        Args:
            file: Загруженный файл

        Returns:
            Относительный путь к сохранённому файлу
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Имя файла отсутствует.',
            )

        if not cls.validate_image_extension(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Недопустимое расширение файла. '
                f'Разрешены: {", ".join(cls.ALLOWED_EXTENSIONS)}',
            )

        content = await file.read()

        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Размер файла превышает {cls.MAX_FILE_SIZE // (1024 * 1024)} MB.',
            )

        ext = Path(file.filename).suffix.lower()
        unique_filename = f'{uuid.uuid4()}{ext}'

        cls.setup_upload_dir()
        file_path = cls.UPLOAD_DIR / unique_filename

        with open(file_path, 'wb') as f:
            f.write(content)

        # Возвращаем относительный путь для URL
        return f'media/recipes/{unique_filename}'

    @classmethod
    def save_base64_image(cls, base64_string: str) -> str:
        """
        Сохранить изображение из base64 строки.

        Args:
            base64_string: Строка в формате "data:image/png;base64,..." или просто base64

        Returns:
            Относительный путь к сохранённому файлу
        """
        try:
            if base64_string.startswith('data:image'):
                header, encoded = base64_string.split(',', 1)
                mime_type = header.split(':')[1].split(';')[0]
                ext = '.' + mime_type.split('/')[-1]

                if ext not in cls.ALLOWED_EXTENSIONS:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Недопустимый формат изображения: {mime_type}',
                    )
            else:
                encoded = base64_string
                ext = '.png'

            image_data = base64.b64decode(encoded)

            if len(image_data) > cls.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Размер изображения превышает '
                    f'{cls.MAX_FILE_SIZE // (1024 * 1024)} MB.',
                )

            unique_filename = f'{uuid.uuid4()}{ext}'

            cls.setup_upload_dir()
            file_path = cls.UPLOAD_DIR / unique_filename

            with open(file_path, 'wb') as f:
                f.write(image_data)

            # Возвращаем относительный путь для URL
            return f'media/recipes/{unique_filename}'

        except (ValueError, base64.binascii.Error) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Некорректная base64 строка: {str(e)}',
            )

    @classmethod
    def delete_image(cls, image_path: str) -> None:
        """Удалить изображение."""
        try:
            # Если путь относительный, делаем его абсолютным от BASE_DIR
            if not image_path.startswith('/'):
                file_path = BASE_DIR / image_path
            else:
                file_path = Path(image_path)

            if file_path.exists() and file_path.is_file():
                file_path.unlink()
        except Exception:
            pass
