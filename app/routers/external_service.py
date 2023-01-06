from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db, crud, schemas

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.ExternalService])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    services = crud.get_external_services(db, skip=skip, limit=limit)
    return services


@router.get("/{service_id}", response_model=schemas.ExternalService)
def read_clients(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_external_service(db, service_id)
    return service


@router.post("/startup", response_model=schemas.ExternalService)
def startup_service(service: schemas.ExternalServiceCreate, db: Session = Depends(get_db)):
    db_service = crud.get_external_service_by_ip(db, ip=service.ip)
    if db_service:
        raise HTTPException(status_code=400, detail="Service already registered")
    return crud.create_external_service(db=db, service=service)
