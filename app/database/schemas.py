import re

from pydantic import BaseModel, validator

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

    @validator('ip')
    def check_ip(cls, v):
        ip_match = re.match(r'^(http(s)?://)(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:\d{1,4})?$', v)
        if ip_match:
            return v
        raise ValueError('invalid host address. Template: http(s)://ip_v4:post')


class ExternalServiceCreate(ExternalServiceBase):
    pass


class ExternalService(ExternalServiceBase):
    id: int

    zones: list[PhoneZoneExternalService] = []

    class Config:
        orm_mode = True
