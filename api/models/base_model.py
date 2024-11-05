from sqlalchemy import text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    BaseModel inherits from SQLAlchemy Base and is also a model for creating
    custom methods like create_schema and create_tables, which will also be inherited
    by models created in api.models.
    """
    __abstract__ = True

    @classmethod
    def create_schema(cls, engine):
        with engine.connect() as connection:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {cls.__tablename__}'))

    @classmethod
    def create_tables(cls, engine):
        cls.create_schema(engine)
        Base.metadata.create_all(engine)
