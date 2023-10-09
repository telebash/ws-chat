from sqlalchemy import func, DateTime, Column
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class BaseModel:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampModel(object):
    created_at = Column(DateTime, default=func.now())
