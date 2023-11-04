from typing import Union

from sqlalchemy import select

from db import Session, User
from schemas.user import UserCreate
from services.auth import hash_password, decode_access_token, decode_refresh_token


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
    await db.close()
    return user


async def get_user_by_email(email: str) -> Union[User | None]:
    db = Session()
    query = select(User).where(User.email == email)
    user = await db.execute(query)
    user = user.scalars().first()
    await db.close()
    return user


def get_username_by_token(token: str, token_type: str) -> str:
    if token_type == "access_token":
        username = decode_access_token(token)
    else:
        username = decode_refresh_token(token)
    return username
