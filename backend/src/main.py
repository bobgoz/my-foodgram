from fastapi import FastAPI
import uvicorn
from src.routers.tags import router as tag_router
from src.routers.ingredients import router as ingredient_router
from src.routers.users import router as user_router

app = FastAPI(title='Foodgram-bobgoz')
app.include_router(tag_router)
app.include_router(ingredient_router)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run(app)
