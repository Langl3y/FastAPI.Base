# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from be.env import *
from api.models.base_model import Base

db_url = f'{db_manager}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Create a db session instance and return it for interacting the database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_database():
    """
    Create all tables from defined models in api.models
    """
    Base.metadata.create_all(bind=engine)
