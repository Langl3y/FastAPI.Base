from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class GetWeatherInfoSerializer(BaseModel):
    id: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    timestamp: Optional[int] = None
    timezone: Optional[str] = None
    sunrise: Optional[int] = None
    sunset: Optional[int] = None
    temp: Optional[float] = None
    feels_like: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[float] = None
    dew_point: Optional[float] = None
    uvi: Optional[float] = None
    clouds: Optional[float] = None
    visibility: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_deg: Optional[float] = None
    wind_gust: Optional[float] = None
    weather: Optional[str] = None
    pop: Optional[float] = None


class CreateWeatherInfoSerializer(BaseModel):
    lat: float
    lon: float


class UpdateWeatherInfoSerializer(GetWeatherInfoSerializer):
    id: int


class DeleteWeatherInfoSerializer(BaseModel):
    id: int


class WeatherResponseSerializer(GetWeatherInfoSerializer):

    class Config:
        from_attributes = True