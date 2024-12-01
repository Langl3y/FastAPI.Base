from sqlalchemy.orm import Session
from sqlalchemy import and_
from api.models.tasks import Task
from api.common.responses import APIResponseCode


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_tasks(self, page: int, page_size: int, data_body):
        try:
            query = self.db.query(Task).filter(Task.is_deleted == False)
            filters = []

            data_dict = data_body.dict(exclude={'access_token', 'page', 'page_size'})
            for key, value in data_dict.items():
                if value is not None:
                    filters.append(getattr(Task, key) == value)

            if filters:
                query = query.filter(and_(*filters))

            total = query.count()
            offset = (page - 1) * page_size if total > 0 else 0
            results = query.offset(offset).limit(page_size).all()
            total_pages = (total + page_size - 1) // page_size

            return results, total, page, page_size, total_pages
        except Exception as e:
            self.db.rollback()
            raise Exception(f"{APIResponseCode.DATABASE_ERROR['message']}: {str(e)}")

    def create_task(self, data_body):
        try:
            task = Task(**data_body.dict(exclude={'access_token'}))
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception as e:
            self.db.rollback()
            raise Exception(f"{APIResponseCode.DATABASE_ERROR['message']}: {str(e)}")

    def update_task(self, data_body):
        try:
            task = self.db.query(Task).filter(
                Task.id == data_body.id,
                Task.is_deleted == False
            ).first()
            
            if task is None:
                raise ValueError(f"{APIResponseCode.NOT_FOUND['message']}: Task with id {data_body.id}")

            update_data = data_body.dict(exclude={'access_token', 'id'})
            for key, value in update_data.items():
                if value is not None:
                    setattr(task, key, value)
                    
            self.db.commit()
            self.db.refresh(task)
            return task
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_task(self, data_body):
        try:
            task = self.db.query(Task).filter(
                Task.id == data_body.id,
                Task.is_deleted == False
            ).first()
            
            if task is None:
                raise ValueError(f"{APIResponseCode.NOT_FOUND['message']}: Task with id {data_body.id}")

            task.is_deleted = True
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e
