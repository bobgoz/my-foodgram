from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from async_foodgram.app.config import BASE_DIR

from .routers import (
    auth_router,
    ingredient_router,
    recipe_router,
    tag_router,
    user_router,
)

app = FastAPI(
    title='Foodgram-bobgoz',
    root_path='/api',
)

media_dir = BASE_DIR / 'media'
media_dir.mkdir(exist_ok=True)
app.mount('/media', StaticFiles(directory=str(media_dir)), name='media')

add_pagination(app)

app.include_router(tag_router)
app.include_router(ingredient_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(recipe_router)
