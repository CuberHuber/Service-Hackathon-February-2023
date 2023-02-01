from functools import lru_cache

from fastapi import FastAPI

from .config import Settings
from .routers import v1

app = FastAPI()

app.include_router(v1.router)


@lru_cache()
def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "Hello. It's a UVC - unified verification center"}
