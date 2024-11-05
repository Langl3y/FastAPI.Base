from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from api.serializers import GetTasksSerializer, CreateTaskSerializer, UpdateTaskSerializer, DeleteTaskSerializer, TaskResponseSerializer
from api.services import TaskService
from api.common.responses import APIResponseCode
from api.common.utils import get_db

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_router.post('/get_tasks', response_model=dict)
async def get_tasks_router(data_body: Optional[GetTasksSerializer] = None, db: Session = Depends(get_db)):
    try:
        task_service = TaskService(db)

        tasks, total_tasks, page, page_size, total_pages = task_service.get_tasks(
            id=data_body.id if data_body else None,
            user_id=data_body.user_id if data_body else None,
            title=data_body.title if data_body else None,
            description=data_body.description if data_body else None,
            due_date=data_body.due_date if data_body else None,
            status=data_body.status if data_body else None,
            page=data_body.page if data_body and data_body.page else 1,
            page_size=data_body.page_size if data_body and data_body.page_size else 10,
            created_at=data_body.created_at if data_body else None,
            updated_at=data_body.updated_at if data_body else None,
            is_deleted=data_body.is_deleted if data_body else None
        )
        paginated_result = {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_tasks": total_tasks,
            "tasks": [TaskResponseSerializer.from_orm(task).dict() for task in tasks] if tasks else []
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
