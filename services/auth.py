import traceback
from datetime import datetime, timedelta
from typing import Union, Any

import bcrypt
from jose import jwt
from loguru import logger
from services.utils import send_to_connection
from core.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject), "type": "access_token"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject), "type": "refresh_token"}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        if payload.get("type") != "access_token":
            raise Exception("Token is not a access token")
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.JWTError as e:
        raise Exception(e)


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        if payload.get("type") != "refresh_token":
            raise Exception("Token is not a refresh token")
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.JWTError as e:
        raise Exception(e)


async def auth_check_and_get_user(connection_id: str, command: str, token: str):
    from services.user import get_user_by_username
    try:
        username = decode_access_token(token)
        user = await get_user_by_username(username)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': command,
            'status': 'error',
            'body': 'Error reading user'
        }
        send_to_connection(connection_id, message)
        message_for_log = message['body'] + ' ' + error_info
        logger.info(message_for_log)
        raise e

    if user is None:
        message = {
            'command': command,
            'status': 'error',
            'body': 'User not authorization'
        }
        send_to_connection(connection_id, message)

    return user
