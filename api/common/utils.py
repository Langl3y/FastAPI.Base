# -*- coding: utf-8 -*-
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from be.env import *
from api.models.base_model import Base
from api.models import User
from .responses import APIResponseCode


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
    db = SessionLocal()
    create_admin(db)
    """
    Create all tables from defined models in api.models
    """
    Base.metadata.create_all(bind=engine)


def create_admin(db: SessionLocal):
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin = User(
            username="admin",
            password=hash_password(admin_password),
            role="admin"
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)
        db.close()


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

    return hashed_password


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
        return encoded_jwt
    except Exception as e:
        raise Exception(f"{APIResponseCode.SERVER_ERROR['message']}: {str(e)}")


def decode_jwt(access_token: str):
    try:
        payload = jwt.decode(access_token, secret, algorithms=[algorithm])
        return payload
    except jwt.InvalidTokenError as e:
        return e


async def validate_token(access_token: str) -> dict:
    try:
        decoded = jwt.decode(
            access_token,
            key=secret,
            algorithms=[algorithm]
        )
        return {"valid": True, "data": decoded}
    except jwt.ExpiredSignatureError:
        return {
            "valid": False, 
            "error": APIResponseCode.TOKEN_EXPIRED["message"]
        }
    except jwt.InvalidSignatureError:
        return {
            "valid": False, 
            "error": APIResponseCode.INVALID_TOKEN["message"]
        }
    except Exception as e:
        print(f"Token validation error: {str(e)}")  # Debug print
        return {
            "valid": False, 
            "error": f"{APIResponseCode.SERVER_ERROR['message']}: {str(e)}"
        }
