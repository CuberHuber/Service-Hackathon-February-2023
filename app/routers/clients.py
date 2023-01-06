from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from httpx import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..config import Settings
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
    action_phone: str


class Client(Action):
    phone: str


class ActionResponse(Action):
    resp: str
    is_service: bool


def action_request(host: str, action: Client) -> Response | None:
    with httpx.Client(base_url=host, timeout=httpx.Timeout(1.0, connect=2.0)) as client:
        print(host, action)
        try:
            resp: Response = client.request("GET", url=Settings().ex_service_check_action_url, json=action)
            return resp
        except:
            return None


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


@router.put("/action", response_model=ActionResponse)
def check_action(action: Action, db: Session = Depends(get_db)):
    client = crud.get_client(db=db, client_id=action.client_id)
    db_service = crud.get_external_service_by_phone_zone(db=db, phone=action.action_phone)
    if db_service:
        resp = action_request(db_service.__dict__['ip'], Client(**action.dict(), phone=client.__dict__['phone']))
        if resp:
            return ActionResponse(**action.dict(), resp=resp, is_service=True)
        else:
            return ActionResponse(**action.dict(), resp="NON", is_service=True)
    else:
        return ActionResponse(**action.dict(), resp="NON", is_service=False)
