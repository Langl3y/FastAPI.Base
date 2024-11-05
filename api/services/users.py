from sqlalchemy.orm import Session
from sqlalchemy import and_
from api.models import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self, id=None, username=None, created_at=None, updated_at=None, is_deleted=None):
        query = self.db.query(User)
        filters = []

        # Filter incoming data
        if id is not None:
            filters.append(User.id == id)
        if username is not None:
            filters.append(User.username == username)
        if created_at is not None:
            filters.append(User.created_at == created_at)
        if updated_at is not None:
            filters.append(User.updated_at == updated_at)
        if is_deleted is not None:
            filters.append(User.is_deleted == is_deleted)

        if filters:
            query = query.filter(and_(*filters))

        return query.all()

    def create_user(self, data_body):
        new_user = User(**data_body.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def update_user(self, data_body):
        user_obj = self.db.query(User).filter(User.id == data_body.id).first()

        if user_obj is not None:
            for key, value in data_body:
                if value is not None and key != 'id':  # exclude id from mutable fields
                    setattr(user_obj, key, value)
            self.db.commit()
            self.db.refresh(user_obj)

            return user_obj
        return None

    def delete_user(self, user_id):
        user_obj = self.db.query(User).filter(User.id == user_id).first()

        if user_obj is not None:
            setattr(user_obj, "is_deleted", True)
            self.db.commit()
            self.db.refresh(user_obj)

            return True
        return False
