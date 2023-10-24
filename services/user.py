from typing import Union

from jose import jwt
from sqlalchemy import select

from db import Session, User
from schemas.user import UserCreate
from services.auth import decode_access_token
from services.utils import hash_password
from settings import settings


async def create_user(data: UserCreate) -> User:
    db = Session()
    hashed_password = hash_password(data.password)
    user = User(
        username=data.username,
        password=hashed_password,
        email=data.email,
    )
    db.add(user)
    await db.flush()
    await db.commit()
    return user


async def get_user_by_username(username: str) -> Union[User | None]:
    db = Session()
    query = select(User).where(User.username == username)
    user = await db.execute(query)
    user = user.scalars().first()
    await db.commit()
    return user


async def get_user_by_email(email: str) -> Union[User | None]:
    db = Session()
    query = select(User).where(User.email == email)
    user = await db.execute(query)
    user = user.scalars().first()
    await db.commit()
    return user


async def get_user_by_token(token: str) -> Union[User | None]:
    username = decode_access_token(token)
    user = await get_user_by_username(username)
    return user
