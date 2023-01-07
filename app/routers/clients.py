from fastapi import APIRouter, Depends, HTTPException, Body
from httpx import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..config import Settings
import httpx
from ..database import get_db, crud, schemas
import re

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)

HOST_REGEX = r'^(http(s)?://)(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:\d{1,4})?$'


class Action(BaseModel):
    client_id: int
    action_type: str
    action_phone: str


class Client(Action):
    phone: str


class ActionResponse(Action):
    resp: bool
    comment: str
    is_service: bool


def action_request(host: str, action: Client) -> Response:
    try:
        with httpx.Client(base_url=host, timeout=0.2) as client:
            resp = client.get(url=Settings().ex_service_check_action_url + f'{action.phone}')
            return resp
    except httpx.TimeoutException:
        return Response(404)


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
        s_ip = db_service.__dict__['ip']
        s_phone = client.__dict__['phone']
        if re.match(HOST_REGEX, s_ip):
            resp = action_request(s_ip, Client(**action.dict(), phone=s_phone))
            if resp.status_code == 200:
                try:
                    check_resp: bool = resp.json()['check']
                except:
                    check_resp: bool = False
                return ActionResponse(**action.dict(), resp=check_resp, comment=("OK" if check_resp else 'NO'),
                                      is_service=True)

        return ActionResponse(**action.dict(), resp=False, comment="NON", is_service=True)
    else:
        return ActionResponse(**action.dict(), resp=False, comment="NON", is_service=False)
