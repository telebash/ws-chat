from typing import Union

from jose import jwt
from sqlalchemy import select

from db import Session, User
from schemas.user import UserCreate
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


async def get_current_user(token: str) -> Union[User | None]:
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        options={"verify_aud": False},
    )
    username: str = payload.get("sub")
    return await get_user_by_username(username)
