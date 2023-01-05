from sqlalchemy.orm import Session

from . import models, schemas


# добавить после первых тестов
# def addEntry(db: Session, db_entry):
#     db.add(db_entry)
#     db.commit()
#     db.refresh(db_entry)
#     return db_entry


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_phone_number(db: Session, phone: str):
    return db.query(models.Client).filter(models.Client.phone == phone).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate):
    # Пока тут нет генерации токена, но его нужно будет добавить
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_external_service(db: Session, service_id: int):
    return db.query(models.ExternalService).filter(models.ExternalService.id == service_id).first()


def get_external_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ExternalService).offset(skip).limit(limit).all()


def get_external_service_by_phone_zone(db: Session, phone: str):
    """ Дописать нахождение сервиса по номеру зоны"""
    pass


def get_external_service_by_ip(db: Session, ip: str):
    return db.query(models.ExternalService).filter(models.ExternalService.ip == ip).first()


def create_external_service(db: Session, service: schemas.ExternalServiceCreate):
    # Добавить авторизацию сервиса
    db_service = models.ExternalService(**service.dict(),)
    print(db_service.name, db_service.ip)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_phone_zones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PhoneZoneExternalService).offset(skip).limit(limit).all()


def get_phone_zones_by_service_id(db: Session, service_id):
    return db.query(models.PhoneZoneExternalService).filter(models.PhoneZoneExternalService.owner_id == service_id).all()


def get_phone_zone_by_phone(db: Session, phone):
    return db.query(models.PhoneZoneExternalService).filter(models.PhoneZoneExternalService.template == phone).first()


def create_phone_zone(db: Session, phone_zone: schemas.PhoneZoneExternalServiceCreate, service_id: int):
    db_zone = models.PhoneZoneExternalService(template=phone_zone.template, owner_id=service_id)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone


