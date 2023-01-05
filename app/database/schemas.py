from pydantic import BaseModel

"""Client Schema"""


class ClientBase(BaseModel):
    name: str
    phone: str


class ClientCreate(ClientBase):
    password: str


class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True


"""Phone Zone for External Service Schema"""


class PhoneZoneExternalServiceBase(BaseModel):
    template: str


class PhoneZoneExternalServiceCreate(PhoneZoneExternalServiceBase):
    pass


class PhoneZoneExternalService(PhoneZoneExternalServiceBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


"""External Service Schema"""


class ExternalServiceBase(BaseModel):
    name: str
    ip: str


class ExternalServiceCreate(ExternalServiceBase):
    pass


class ExternalService(ExternalServiceBase):
    id: int

    zones: list[PhoneZoneExternalService] = []

    class Config:
        orm_mode = True
