from typing import Generator

from loguru import logger
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db import Session
from services.auth import decode_access_token
from services.user import get_user_by_username

security = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    handle_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = decode_access_token(token.credentials)
    except Exception as e:
        logger.error(e)
        raise handle_exception

    user = await get_user_by_username(username)

    if not user:
        logger.error('User not found')
        raise handle_exception

    return user


async def get_db() -> Generator:
    async with Session() as session:
        yield session
