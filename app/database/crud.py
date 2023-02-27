from sqlalchemy.orm import Session
from enum import Enum
from typing import Any

from . import models


class PluralModule(Enum):
    people = models.Person
    vehicles = models.Vehicle
    officers = models.Officer
    fines = models.Fine


def get_record(db: Session, model_name: str, record_id: int) -> models.Base:
    current_model = PluralModule[model_name].value
    return db.query(current_model).get(record_id)


def list_records(db: Session, model_name: str) -> list[models.Base]:
    return db.query(PluralModule[model_name].value).all()


def get_record_by_field(db: Session, model_name: str, field: str, value: Any) -> models.Base:
    current_model = PluralModule[model_name].value
    return db.query(current_model).filter(getattr(current_model, field) == value).first()


def create_record(db: Session, model_name: str, data: dict) -> models.Base:
    current_model = PluralModule[model_name].value
    record = current_model(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_record(db: Session, model_name: str, data: dict, record_id: int) -> models.Base:
    current_model = PluralModule[model_name].value
    db.query(current_model).filter(current_model.id == record_id).update(data)
    db.commit()
    record = current_model(**data)
    return record


def delete_record(db: Session, model_name: str, record_id: int) -> None:
    current_model = PluralModule[model_name].value
    db.query(current_model).filter(current_model.id == record_id).delete()
    db.commit()


def list_fines(db: Session, email: str) -> list[dict]:
    data = db.query(models.Fine).join(models.Vehicle).join(models.Person).filter(models.Person.email == email).all()
    return [
        {
            "id": record.id,
            "placa_patente": record.vehicle.licence_plate,
            "timestamp": record.date_created,
            "comentarios": record.comments,
        }
        for record in data
    ]
