from datetime import datetime
from sqlalchemy import Integer, Float, String, DateTime, Boolean, Column, ForeignKey, TIMESTAMP
from .base_model import BaseModel
from enum import Enum


class WeatherInfo(BaseModel):
    __tablename__ = "weather_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(Integer, ForeignKey('cities.id'), nullable=False)
    sunrise = Column(TIMESTAMP, nullable=False)
    sunset = Column(TIMESTAMP, nullable=False)
    temp = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    dew_point = Column(Float, nullable=False)
    uvi = Column(Float, nullable=False)
    clouds = Column(Float, nullable=False)
    visibility = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_deg = Column(Float, nullable=False)
    wind_gust = Column(Float, nullable=False)
    weather = Column(String, nullable=False)
    pop = Column(Float, nullable=False)
