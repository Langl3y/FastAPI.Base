from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from api.serializers import GetTasksSerializer, CreateTaskSerializer, UpdateTaskSerializer, DeleteTaskSerializer, TaskResponseSerializer
from api.services import TaskService
from api.common.responses import APIResponseCode
from api.common.utils import get_db, validate_token

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_router.post('/get_tasks', response_model=dict)
async def get_tasks_router(data_body: Optional[GetTasksSerializer] = None, db: Session = Depends(get_db)):
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

        task_service = TaskService(db)
        result, total, page, page_size, total_pages = task_service.get_tasks(
            page, page_size, data_body
        )

        return {
            'response': APIResponseCode.SUCCESS,
            'result': {
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'total_items': total,
                'data': [TaskResponseSerializer.from_orm(item).dict() for item in result]
            }
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@tasks_router.post('/create_task', response_model=dict)
async def create_task_router(data_body: Optional[CreateTaskSerializer], db: Session = Depends(get_db)):
    try:
        task_service = TaskService(db)
        result = task_service.create_task(data_body)

        task_responses = TaskResponseSerializer.from_orm(result).dict() if result else {}
        return {
            'response': APIResponseCode.SUCCESS,
            'result': task_responses
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@tasks_router.post('/update_task', response_model=dict)
async def update_task_router(data_body: Optional[UpdateTaskSerializer], db: Session = Depends(get_db)):
    try:
        task_service = TaskService(db)
        result = task_service.update_task(data_body)

        updated_task_response = TaskResponseSerializer.from_orm(result).dict() if result else {}
        return {
            'response': APIResponseCode.SUCCESS if updated_task_response != {} else APIResponseCode.NOT_FOUND,
            'result': updated_task_response
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }


@tasks_router.post('/delete_task', response_model=dict)
async def delete_task_router(data_body: Optional[DeleteTaskSerializer], db: Session = Depends(get_db)):
    try:
        task_service = TaskService(db)
        result = task_service.delete_task(data_body)

        return {
            'response': APIResponseCode.SUCCESS if result else APIResponseCode.NOT_FOUND,
            'result': result if result else {}
        }
    except Exception as e:
        return {
            'response': APIResponseCode.SERVER_ERROR,
            'error': str(e)
        }
