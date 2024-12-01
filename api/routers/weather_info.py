import jwt

from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from api.serializers import GetWeatherInfoSerializer, CreateWeatherInfoSerializer, UpdateWeatherInfoSerializer, \
    DeleteWeatherInfoSerializer, WeatherResponseSerializer

from be.env import *
from api.services import WeatherService
from api.common.responses import APIResponseCode
from api.common.utils import get_db


weather_info_router = APIRouter(prefix="/weather_info", tags=["weather_info"])


@weather_info_router.post('/get_weather_info', response_model=dict)
async def get_weather_info_router(data_body: Optional[GetWeatherInfoSerializer] = None, db: Session = Depends(get_db)):
    try:
        try:
            decoded = jwt.decode(data_body.access_token, secret=secret, algorithms=[algorithm])
            print("Token is valid:", decoded)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid token.")

        page = data_body.page if data_body and data_body.page else 1
        page_size = data_body.page_size if data_body and data_body.page_size else 10
        result, total, page, page_size, total_pages = WeatherService(db).get_weather_info(page, page_size, data_body)

        weather_info = [WeatherResponseSerializer.from_orm(weather) for weather in result]

        paginated_result = {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "data": [WeatherResponseSerializer.from_orm(info).dict() for info in weather_info] if weather_info else []
        }
        return {
            'response': APIResponseCode.SUCCESS,
            'result': paginated_result
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@weather_info_router.post('/create_weather_info', response_model=dict)
async def create_weather_info_router(data_body: CreateWeatherInfoSerializer, db: Session = Depends(get_db)):
    try:
        try:
            decoded = jwt.decode(data_body.access_token, secret=secret, algorithms=[algorithm])
            print("Token is valid:", decoded)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.InvalidTokenError:
            print("Invalid token.")

        result = WeatherService(db).create_weather_info(data_body)
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
        try:
            decoded_data = jwt.decode(data_body.access_token, secret=secret, algorithms=algorithm)
        except jwt.ExpiredSignatureError as expired_error:
            return {
                "response": APIResponseCode.FAILURE,
                "error": expired_error
            }

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
        try:
            decoded_data = jwt.decode(data_body.access_token, secret=secret, algorithms=algorithm)
        except jwt.ExpiredSignatureError as expired_error:
            return {
                "response": APIResponseCode.FAILURE,
                "error": expired_error
            }

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
