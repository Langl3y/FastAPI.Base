from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from api.models import TaskStatus


class GetTasksSerializer(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None


class CreateTaskSerializer(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: TaskStatus
    is_deleted: bool = False


class UpdateTaskSerializer(BaseModel):
    """
    task's title is not mutable, so it is not included
    """
    id: int
    user_id: Optional[int] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None


class DeleteTaskSerializer(BaseModel):
    id: int


class TaskResponseSerializer(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    title: Optional[str]
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    """
    Config orm mode to convert SQLAlchemy model to pydantic model
    """
    class Config:
        from_attributes = True
