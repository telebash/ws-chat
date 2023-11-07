import json
import datetime
from asyncio import current_task
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings


def json_encoder(val):
    if isinstance(val, Decimal):
        return str(val)
    elif isinstance(val, datetime.date):
        return val.isoformat()
    raise TypeError()


def json_dumps(d):
    return json.dumps(d, default=json_encoder)


engine = create_async_engine(
    settings.get_async_database_url(),
    pool_pre_ping=True,
    echo=False,
    json_serializer=json_dumps,
)
Session = async_scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False),
    scopefunc=current_task
)
