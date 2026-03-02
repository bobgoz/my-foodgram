from fastapi import FastAPI
import uvicorn
from .routers.tags import router as tag_router

app = FastAPI()
app.include_router(tag_router)

if __name__ == '__main__':
    uvicorn.run(app)
