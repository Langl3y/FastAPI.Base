from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class GetUserSerializer(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None


class CreateUserSerializer(BaseModel):
    username: str
    password: str


class UpdateUserSerializer(BaseModel):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None


class DeleteUserSerializer(BaseModel):
    id: int


class UserResponseSerializer(BaseModel):
    id: Optional[int]
    username: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_deleted: Optional[bool]
    """
    Config orm mode to convert SQLAlchemy model to pydantic model
    """
    class Config:
        from_attributes = True
