from sqlalchemy.orm import Session
from sqlalchemy import and_
from api.models.tasks import Task


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def get_tasks(self, page: int, page_size: int, id=None, user_id=None, title=None, description=None, due_date=None,
                  status=None,
                  created_at=None, updated_at=None, is_deleted=None):
        query = self.db.query(Task)
        filters = []

        # Filter incoming data
        if id is not None:
            filters.append(Task.id == id)
        if user_id is not None:
            filters.append(Task.user_id == user_id)
        if title is not None:
            filters.append(Task.title == title)
        if description is not None:
            filters.append(Task.description == description)
        if due_date is not None:
            filters.append(Task.due_date == due_date)
        if status is not None:
            filters.append(Task.status == status)
        if created_at is not None:
            filters.append(Task.created_at == created_at)
        if updated_at is not None:
            filters.append(Task.updated_at == updated_at)
        if is_deleted is not None:
            filters.append(Task.is_deleted == is_deleted)

        if filters:
            query = query.filter(and_(*filters))

        total_tasks = query.count()

        # Map page number to offset + 1, since offset always starts at 0 and page number starts at 1
        offset = (page - 1) * page_size if total_tasks > 0 else 0

        # Paginate all tasks into chunks of *page_size* objects
        tasks = query.offset(offset).limit(page_size).all()
        total_pages = (total_tasks + page_size - 1) // page_size

        return tasks, total_tasks, page, page_size, total_pages

    def create_task(self, data_body):
        new_task = Task(**data_body.dict())
        self.db.add(new_task)
        self.db.commit()

        return new_task

    def update_task(self, data_body):
        task_obj = self.db.query(Task).filter(Task.id == data_body.id).first()

        if task_obj is not None:
            for key, value in data_body:
                if value is not None and key != 'id':  # to exclude id from mutable fields
                    setattr(task_obj, key, value)
            self.db.commit()
            self.db.refresh(task_obj)

            return task_obj
        return None

    def delete_task(self, data_body):
        task_obj = self.db.query(Task).filter(Task.id == data_body.id).first()

        if task_obj is not None:
            setattr(task_obj, "is_deleted", True)
            self.db.commit()
            self.db.refresh(task_obj)

            return True
        return False
