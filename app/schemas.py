from datetime import datetime
from typing import List
from pydantic import BaseModel


class FineCreate(BaseModel):
    placa_patente: str
    timestamp: datetime
    comentarios: str

class FineList(FineCreate):
    id: int


class Fine(BaseModel):
    id: int
    comments: str
    date_created: datetime
    vehicle_id: int

    class Config:
        orm_mode = True


class VehicleBase(BaseModel):
    licence_plate: str
    brand: str
    color: str
    person_id: int


class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase):
    id: int
    vehicles: List[Fine] | None

    class Config:
        orm_mode = True


class PersonBase(BaseModel):
    name: str
    email: str


class PersonCreate(PersonBase):
    pass


class Person(PersonBase):
    id: int
    vehicles: List[Vehicle] | None

    class Config:
        orm_mode = True


class OfficerLogin(BaseModel):
    identification_number: int


class OfficerBase(BaseModel):
    name: str
    identification_number: int

class OfficerCreate(OfficerBase):
    pass

class Officer(OfficerBase):
    id: int

    class Config:
        orm_mode = True
