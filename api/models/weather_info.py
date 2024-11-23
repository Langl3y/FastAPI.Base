from datetime import datetime
from sqlalchemy import Integer, Float, String, DateTime, Boolean, Column, ForeignKey, TIMESTAMP
from .base_model import BaseModel
from enum import Enum


class WeatherInfo(BaseModel):
    __tablename__ = "weather_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(Integer)
    timezone = Column(String)
    sunrise = Column(Integer)
    sunset = Column(Integer)
    temp = Column(Float)
    feels_like = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    dew_point = Column(Float)
    uvi = Column(Float)
    clouds = Column(Float)
    visibility = Column(Float)
    wind_speed = Column(Float)
    wind_deg = Column(Float)
    wind_gust = Column(Float)
    weather = Column(String)
    pop = Column(Float)
    rain = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)
