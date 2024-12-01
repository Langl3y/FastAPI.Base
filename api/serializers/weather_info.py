from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional
from api.common.responses import APIResponseCode


class GetWeatherInfoSerializer(BaseModel):
    access_token: str
    id: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    timestamp: Optional[int] = None
    timezone: Optional[str] = None
    page: Optional[int] = 1
    page_size: Optional[int] = 10

    @validator('page')
    def validate_page(cls, v):
        if v is not None and v < 1:
            raise ValueError(f"{APIResponseCode.VALIDATION_ERROR['message']}: Page must be greater than 0")
        return v

    @validator('page_size')
    def validate_page_size(cls, v):
        if v is not None and v < 1:
            raise ValueError(f"{APIResponseCode.VALIDATION_ERROR['message']}: Page size must be greater than 0")
        return v


class CreateWeatherInfoSerializer(BaseModel):
    access_token: str
    lat: float
    lon: float

    @validator('lat')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError(f"{APIResponseCode.INVALID_COORDINATES['message']}: Latitude must be between -90 and 90")
        return v

    @validator('lon')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError(f"{APIResponseCode.INVALID_COORDINATES['message']}: Longitude must be between -180 and 180")
        return v


class UpdateWeatherInfoSerializer(BaseModel):
    access_token: str
    id: int
    lat: Optional[float] = None
    lon: Optional[float] = None
    timestamp: Optional[int] = None
    timezone: Optional[str] = None

    @validator('lat')
    def validate_latitude(cls, v):
        if v is not None and not -90 <= v <= 90:
            raise ValueError(f"{APIResponseCode.INVALID_COORDINATES['message']}: Latitude must be between -90 and 90")
        return v

    @validator('lon')
    def validate_longitude(cls, v):
        if v is not None and not -180 <= v <= 180:
            raise ValueError(f"{APIResponseCode.INVALID_COORDINATES['message']}: Longitude must be between -180 and 180")
        return v


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
