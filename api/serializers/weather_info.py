from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class GetWeatherInfoSerializer(BaseModel):
    access_token: str
    id: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    timestamp: Optional[int] = None
    timezone: Optional[str] = None

    page: Optional[int] = None
    page_size: Optional[int] = None


class CreateWeatherInfoSerializer(BaseModel):
    access_token: str
    lat: float
    lon: float


class UpdateWeatherInfoSerializer(GetWeatherInfoSerializer):
    access_token: str
    id: int


class DeleteWeatherInfoSerializer(BaseModel):
    access_token: str
    id: int


class WeatherResponseSerializer(BaseModel):
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

    class Config:
        from_attributes = True
