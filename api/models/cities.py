from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean
from .base_model import BaseModel


class City(BaseModel):
    __tablename__ = "cities"

    id = Column(Integer, index=True, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    timezone = Column(String)
    timezone_offset = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)
