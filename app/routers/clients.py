from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import BaseModel
import httpx
from ..database import get_db, crud, schemas

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)


class Action(BaseModel):
    client_id: int
    action_type: str
    called_phone: str


def action_request(host: str):
    with httpx.Client() as client:
        return client.get(host).json()


@router.get("/", response_model=list[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients


@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_user = crud.get_client_by_phone_number(db, phone=client.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone already registered")
    return crud.create_client(db=db, client=client)


@router.get("/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_client


@router.get("/action")
def check_action(action: Action, db: Session = Depends(get_db)):
    action_data = jsonable_encoder(action)
    client = crud.get_client_by_phone_number(db=db, phone=action_data.phone)
    db_service = crud.get_external_service_by_phone_zone(db=db, phone=action_data.called_phone)

    # дописать поиск сервиса и запрос на его host для получения ответа о событии
    action_request(db_service.ip)
    if db_service:
        raise HTTPException(status_code=404, detail="Phone not exist")

    return True



