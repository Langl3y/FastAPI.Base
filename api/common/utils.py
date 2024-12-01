# -*- coding: utf-8 -*-
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from be.env import *
from be.config import create_admin
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
    create_admin()
    """
    Create all tables from defined models in api.models
    """
    Base.metadata.create_all(bind=engine)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

    return hashed_password


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(access_token: str):
    try:
        payload = jwt.decode(access_token, secret, algorithms=[algorithm])
        return payload
    except jwt.InvalidTokenError as e:
        return e
