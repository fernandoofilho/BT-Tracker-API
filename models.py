from pydantic import BaseModel, Field
from typing import Any
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db import Base
from sqlalchemy.orm import relationship
class PayloadBody(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude between -90 and 90")
    lon: float = Field(..., ge=-180, le=180, description="Longitude between -180 and 180")

class ApiForecastHeader(Base):
    __tablename__ = "ForecastsHeader"
    id = Column(Integer, primary_key=True, index=True)
    modelrun = Column(String, nullable=False)
    name = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    timezone_abbrevation = Column(String, nullable=True)
    latitude = Column(Integer, nullable=True)
    modelrun_utc = Column(String, nullable=True)
    longitude = Column(Integer, nullable=True)
    utc_timeoffset = Column(Integer, nullable=True)
    generation_time_ms = Column(Float, nullable=True)

class Units(Base):
    __tablename__ = "Units"

    id = Column(Integer, primary_key=True, index=True)
    modelrun = Column(String, nullable=False)
    precipitation = Column(String, nullable=True)
    windspeed = Column(String, nullable=True)
    precipitation_probability = Column(String, nullable=True)
    relativehumidity = Column(String, nullable=True)
    temperature = Column(String, nullable=True)
    time = Column(String, nullable=True)
    pressure = Column(String, nullable=True)
    winddirection = Column(String, nullable=True)

class State(Base):
    __tablename__ = "State"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    forecast_items = relationship("ApiForecastItem", back_populates="state")

class ApiForecastItem(Base):
    __tablename__ = "Forecasts"
    id = Column(Integer, primary_key=True, index=True)
    modelrun = Column(String, nullable=False)
    date_forecast = Column(String, nullable=True)
    windspeed = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    precipitation_probability = Column(Float, nullable=True)
    convective_precipitation = Column(Float, nullable=True)
    rainspot = Column(String, nullable=True)
    pictocode = Column(Float, nullable=True)
    felttemperature = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    isdaylight = Column(Float, nullable=True)
    uvindex = Column(Float, nullable=True)
    relativehumidity = Column(Float, nullable=True)
    sealevelpressure = Column(Float, nullable=True)
    winddirection = Column(Float, nullable=True)
    state_id = Column(Integer, ForeignKey("State.id"), nullable=True)
    state = relationship("State", back_populates="forecast_items")

