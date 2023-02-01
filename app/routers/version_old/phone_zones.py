from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, crud, schemas

router = APIRouter(
    prefix="/phone_zones",
    tags=["phone_zone"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/{service_id}/set",
    responses={403: {"description": "Operation forbidden"}},
    response_model=schemas.PhoneZoneExternalService
)
def update_phone_zone(service_id: int, phone_zone: schemas.PhoneZoneExternalServiceCreate, db: Session = Depends(get_db)):
    owner = crud.get_external_service(db, service_id=service_id)
    if owner:
        db_zone = crud.get_phone_zone_by_phone(db=db, phone=phone_zone.template)
        if db_zone:
            raise HTTPException(status_code=400, detail="Phone zone already registered")

        return crud.create_phone_zone(db=db, phone_zone=phone_zone, service_id=service_id)
    else:
        raise HTTPException(status_code=404, detail="External service is not exist")


@router.get("/{service_id}", tags=["phone_zone"], response_model=list[schemas.PhoneZoneExternalService])
def read_phone_zones_by_service_id(service_id: int, db: Session = Depends(get_db)):
    zones = crud.get_phone_zones_by_service_id(db, service_id=service_id)
    return zones


@router.get("/", response_model=list[schemas.PhoneZoneExternalService])
def read_all_zones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    zones = crud.get_phone_zones(db, skip=skip, limit=limit)
    return zones