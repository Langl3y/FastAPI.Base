from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class GetWeatherInfoSerializer(BaseModel):
    id: Optional[int] = None
    city: Optional[int] = None
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


class CreateWeatherInfoSerializer(GetWeatherInfoSerializer):
    pass


class UpdateWeatherInfoSerializer(GetWeatherInfoSerializer):
    pass

class DeleteWeatherInfoSerializer(BaseModel):
    id: Optional[int] = None


class WeatherResponseSerializer(GetWeatherInfoSerializer):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True