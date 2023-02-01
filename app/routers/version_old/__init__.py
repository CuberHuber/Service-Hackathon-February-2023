from fastapi import APIRouter

import app.routers.version_old.clients
import app.routers.version_old.external_service
import app.routers.version_old.phone_zones

router = APIRouter(
    prefix='/v1',
    tags=['v1'],
    responses={404: {"description": "Not found"}},
)

router.include_router(clients.router)
router.include_router(external_service.router)
router.include_router(phone_zones.router)


@router.get("/")
async def root():
    return {"message": "Hello. I'm UVC API v1!"}


