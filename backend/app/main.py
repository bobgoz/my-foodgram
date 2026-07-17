from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers.ingredients import router as ingredient_router
from .routers.tags import router as tag_router
from .routers.users import router as user_router

app = FastAPI(title='Foodgram-bobgoz')

add_pagination(app)

app.include_router(tag_router)
app.include_router(ingredient_router)
app.include_router(user_router)
