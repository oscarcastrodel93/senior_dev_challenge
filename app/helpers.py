from .database import crud
from . import schemas
from sqlalchemy.orm import Session
from enum import Enum
from fastapi import HTTPException


class ValidateFields(Enum):
    people = "email"
    vehicles = "licence_plate"
    officers = "identification_number"


def validate_save(db: Session, module: str, form_data: dict, record_id: int | None = None) -> None:
    """
    Validates if a record can be saved given a model name and a expected unique field.
    When updating (record_id present), validates if a db record exists and if that db record id it's different from incoming one.
    When creating, just validates if exists a record on the db with specified data.
    """
    validate_field = ValidateFields[module].value
    validate_value = form_data.get(validate_field)
    existing_record = crud.get_record_by_field(
        db, model_name=module, field=validate_field, value=validate_value
    )
    if (record_id and existing_record and existing_record.id != record_id) or (not record_id and existing_record):
        raise HTTPException(status_code=400, detail=f"Este registro ya existe: {validate_value}.")


def check_officer(db: Session, officer_data: schemas.OfficerLogin):
    """
    Checks if an officer exists given identification_number.

    TODO: add password to officer model
    """
    return crud.get_record_by_field(
        db, model_name="officers", field="identification_number", value=officer_data.identification_number
    )

    