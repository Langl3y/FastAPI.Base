from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from api.serializers import GetUserSerializer, CreateUserSerializer, UpdateUserSerializer, DeleteUserSerializer, UserResponseSerializer
from api.services import UserService
from api.common.responses import APIResponseCode
from api.common.utils import get_db

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post('/get_users', response_model=dict)
async def get_users_router(data_body: Optional[GetUserSerializer] = None, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)

        result = user_service.get_users(
            id=data_body.id if data_body else None,
            username=data_body.username if data_body else None,
            created_at=data_body.created_at if data_body else None,
            updated_at=data_body.updated_at if data_body else None,
            is_deleted=data_body.is_deleted if data_body else None
        )

        user_responses = [UserResponseSerializer.from_orm(user) for user in result] if result else []
        return {
            'response': APIResponseCode.SUCCESS,
            'result': user_responses
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@users_router.post('/create_user', response_model=dict)
async def create_user_router(data_body: CreateUserSerializer, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        result = user_service.create_user(data_body)

        user_response = UserResponseSerializer.from_orm(result).dict() if result else {}
        return {
            'response': APIResponseCode.SUCCESS,
            'result': user_response
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@users_router.post('/update_user', response_model=dict)
async def update_user_router(data_body: Optional[UpdateUserSerializer], db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        result = user_service.update_user(data_body)

        updated_user_response = UserResponseSerializer.from_orm(result).dict() if result else {}
        return {
            'response': APIResponseCode.SUCCESS if updated_user_response != {} else APIResponseCode.NOT_FOUND,
            'result': updated_user_response
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@users_router.post('/delete_user', response_model=dict)
async def delete_user_router(data_body: Optional[DeleteUserSerializer], db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        result = user_service.delete_user(data_body)

        return {
            'response': APIResponseCode.SUCCESS if result else APIResponseCode.NOT_FOUND,
            'result': result if result else {}
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }
