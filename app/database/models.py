from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from .db import Base


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    vehicles = relationship("Vehicle", back_populates="owner")


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    licence_plate = Column(String, unique=True, index=True, nullable=False)
    brand = Column(String, index=True, nullable=False)
    color = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("people.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Person", back_populates="vehicles")
    fines = relationship("Fine", back_populates="vehicle")


class Officer(Base):
    __tablename__ = "officers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    identification_number = Column(Integer, unique=True, index=True, nullable=False)


class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    comments = Column(Text)
    date_created = Column(DateTime, index=True, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    
    vehicle = relationship("Vehicle", back_populates="fines")
