from sqlalchemy import Column, VARCHAR, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class ExternalService(Base):
    __tablename__ = "external_service"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(VARCHAR(22), unique=True, index=True)
    name = Column(VARCHAR(50), unique=True, index=True)

    zones = relationship("PhoneZoneExternalService", back_populates="owner")


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(50), unique=True, index=True)
    phone = Column(VARCHAR(22), unique=True, index=True)
    token = Column(VARCHAR(260))
    password = Column(VARCHAR(1000), unique=True)


class PhoneZoneExternalService(Base):
    __tablename__ = "phone_zone_external_service"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("external_service.id"))
    template = Column(VARCHAR(50), unique=True, index=True)

    owner = relationship("ExternalService", back_populates="zones")
