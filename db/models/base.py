from sqlalchemy import func, DateTime, Column
from sqlalchemy.orm import declared_attr, DeclarativeBase


class BaseModel(DeclarativeBase):
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimestampModel(object):
    created_at = Column(DateTime, default=func.now())
