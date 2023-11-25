from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import Session, User
from schemas.user import UserCreate
from services.auth import hash_password


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


async def delete_user(id: int):
    db = Session()
    user = await db.get(User, id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    await db.close()
    return True


async def change_user_password(id: int, new_password: str):
    db = Session()
    user = await db.get(User, id)
    if not user:
        return None
    user.password = hash_password(new_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await db.close()
    return user


async def update_avatar_user(id: int, image_url: str):
    db = Session()
    user = await db.get(User, id)
    if not user:
        return None
    user.image_url = image_url
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await db.close()
    return user


async def user_active(id: int):
    db = Session()
    user = await db.get(User, id)
    if not user:
        return None
    user.is_active = True
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await db.close()
    return user


async def user_paid(id: int) -> None:
    db = Session()
    user = await db.get(User, id)
    if not user:
        return
    user.paid = True
    user.subscription_date = datetime.now()
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await db.close()
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


async def get_user(id: int):
    db = Session()
    user = await db.get(User, id)
    await db.close()
    return user
