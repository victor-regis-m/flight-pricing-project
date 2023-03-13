from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class FlightInfo(Base):
    __tablename__ = "flight_info"
    id = Column(Integer, primary_key=True)
    duration = Column(String)
    price = Column(Integer)
    stops = Column(Integer)
    operator = Column(String)
    departure_airport = Column(String)
    arrival_airport = Column(String)
    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)
