from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .routers import (
    auth_router,
    ingredient_router,
    tag_router,
    user_router,
)

app = FastAPI(title='Foodgram-bobgoz')

add_pagination(app)

app.include_router(tag_router)
app.include_router(ingredient_router)
app.include_router(user_router)
app.include_router(auth_router)
