from functools import lru_cache

from fastapi import Depends, FastAPI

# from .dependencies import *
from .routers import clients, external_service, phone_zones
from .config import Settings

# app = FastAPI(dependencies=[Depends(*)])

app = FastAPI()

app.include_router(clients.router)
app.include_router(external_service.router)
app.include_router(phone_zones.router)


@lru_cache()
def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
