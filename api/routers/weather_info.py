import jwt

from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from api.serializers import GetWeatherInfoSerializer, CreateWeatherInfoSerializer, UpdateWeatherInfoSerializer, \
    DeleteWeatherInfoSerializer, WeatherResponseSerializer

from be.env import *
from api.services import WeatherService
from api.common.responses import APIResponseCode
from api.common.utils import get_db, validate_token

weather_info_router = APIRouter(prefix="/weather_info", tags=["weather_info"])


@weather_info_router.post('/get_weather_info', response_model=dict)
async def get_weather_info_router(data_body: Optional[GetWeatherInfoSerializer] = None, db: Session = Depends(get_db)):
    try:
        if not data_body or not data_body.access_token:
            return {
                'response': APIResponseCode.MISSING_TOKEN,
                'error': APIResponseCode.MISSING_TOKEN["message"]
            }

        token_result = await validate_token(data_body.access_token)
        if not token_result["valid"]:
            return {
                'response': APIResponseCode.INVALID_TOKEN,
                'error': token_result["error"]
            }

        page = data_body.page or 1
        page_size = data_body.page_size or 10

        weather_service = WeatherService(db)
        result, total, page, page_size, total_pages = weather_service.get_weather_info(
            page, page_size, data_body
        )

        return {
            'response': APIResponseCode.SUCCESS,
            'result': {
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'total_items': total,
                'data': [WeatherResponseSerializer.from_orm(item).dict() for item in result]
            }
        }
    except ValueError as ve:
        return {
            'response': APIResponseCode.VALIDATION_ERROR,
            'error': str(ve)
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@weather_info_router.post('/create_weather_info', response_model=dict)
async def create_weather_info_router(data_body: CreateWeatherInfoSerializer, db: Session = Depends(get_db)):
    try:
        if not data_body.access_token:
            return {
                'response': APIResponseCode.MISSING_TOKEN,
                'error': APIResponseCode.MISSING_TOKEN["message"]
            }

        token_result = await validate_token(data_body.access_token)
        if not token_result["valid"]:
            return {
                'response': APIResponseCode.INVALID_TOKEN,
                'error': token_result["error"]
            }

        weather_service = WeatherService(db)
        result = weather_service.create_weather_info(data_body)

        return {
            'response': APIResponseCode.SUCCESS,
            'result': WeatherResponseSerializer.from_orm(result).dict()
        }
    except ValueError as ve:
        return {
            'response': APIResponseCode.VALIDATION_ERROR,
            'error': str(ve)
        }
    except Exception as e:
        if "API key" in str(e):
            return {
                'response': APIResponseCode.API_ERROR,
                'error': str(e)
            }
        elif "rate limit" in str(e).lower():
            return {
                'response': APIResponseCode.RATE_LIMIT_EXCEEDED,
                'error': str(e)
            }
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@weather_info_router.post('/update_weather_info', response_model=dict)
async def update_weather_info_router(data_body: UpdateWeatherInfoSerializer, db: Session = Depends(get_db)):
    try:
        if not data_body or not data_body.access_token:
            return {
                'response': APIResponseCode.MISSING_TOKEN,
                'error': APIResponseCode.MISSING_TOKEN["message"]
            }

        token_result = await validate_token(data_body.access_token)
        if not token_result["valid"]:
            return {
                'response': APIResponseCode.INVALID_TOKEN,
                'error': token_result["error"]
            }

        weather_service = WeatherService(db)
        result = weather_service.update_weather_info(data_body)

        if not result:
            return {
                'response': APIResponseCode.NOT_FOUND,
                'error': f'Weather info with id {data_body.id} not found'
            }

        return {
            'response': APIResponseCode.SUCCESS,
            'result': WeatherResponseSerializer.from_orm(result).dict()
        }
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")  # Debug print
        return {
            'response': APIResponseCode.VALIDATION_ERROR,
            'error': str(ve)
        }
    except Exception as e:
        print(f"Update error: {str(e)}")  # Debug print
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
