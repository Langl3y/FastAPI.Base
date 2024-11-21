from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from api.serializers import GetWeatherInfoSerializer, CreateWeatherInfoSerializer, UpdateWeatherInfoSerializer, DeleteWeatherInfoSerializer, WeatherResponseSerializer
from api.services import WeatherService
from api.common.responses import APIResponseCode
from api.common.utils import get_db


weather_info_router = APIRouter(prefix="/weather_info", tags=["weather_info"])


@weather_info_router.post('/get_weather_info', response_model=dict)
async def get_weather_info_router(data_body: Optional[GetWeatherInfoSerializer] = None, db: Session = Depends(get_db)):
    try:
        weather_service = WeatherService(db)

        result = weather_service.get_weather_info(
            id=data_body.id if data_body else None,
            city=data_body.city if data_body else None,
            sunrise=data_body.sunrise if data_body else None,
            sunset=data_body.sunset if data_body else None,
            temp=data_body.temp if data_body else None,
            feels_like=data_body.feel_l if data_body else None,
            pressure=data_body.pressure if data_body else None,
            humidity=data_body.humidity if data_body else None,
            dew_point=data_body.dew_point if data_body else None,
            uvi=data_body.uvi if data_body else None,
            clouds=data_body.clouds if data_body else None,
            visibility=data_body.visibility if data_body else None,
            wind_speed=data_body.wind_speed if data_body else None,
            wind_deg=data_body.wind_deg if data_body else None,
            wind_gust=data_body.wind_gust if data_body else None,
            weather=data_body.weather if data_body else None,
            pop=data_body.pop if data_body else None,
        )

        weather_responses = [WeatherResponseSerializer.from_orm(weather) for weather in result] if result else []
        return {
            'response': APIResponseCode.SUCCESS,
            'result': weather_responses
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@weather_info_router.post('/create_weather_info', response_model=dict)
async def create_weather_info_router(data_body: CreateWeatherInfoSerializer, db: Session = Depends(get_db)):
    try:
        weather_service = WeatherService(db)
        result = weather_service.create_weather_info(data_body)

        weather_response = WeatherResponseSerializer.from_orm(result).dict() if result else {}
        return {
            'response': APIResponseCode.SUCCESS,
            'result': weather_response
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@weather_info_router.post('/update_weather_info', response_model=dict)
async def update_weather_info_router(data_body: Optional[UpdateWeatherInfoSerializer], db: Session = Depends(get_db)):
    try:
        weather_service = WeatherService(db)
        result = weather_service.update_weather_info(data_body)

        updated_weather_info = WeatherResponseSerializer.from_orm(result).dict() if result else {}
        return {
            'response': APIResponseCode.SUCCESS if updated_weather_info != {} else APIResponseCode.NOT_FOUND,
            'result': updated_weather_info
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@weather_info_router.post('/delete_weather_info', response_model=dict)
async def delete_user_router(data_body: Optional[DeleteWeatherInfoSerializer], db: Session = Depends(get_db)):
    try:
        weather_service = WeatherService(db)
        result = weather_service.delete_weather_info(data_body)

        return {
            'response': APIResponseCode.SUCCESS if result else APIResponseCode.NOT_FOUND,
            'result': result if result else {}
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }
