import traceback

from email_validator import validate_email, EmailNotValidError
from loguru import logger

from dispatcher import AsyncDispatcher
from schemas.token import Token
from schemas.user import UserCreate, UserLogin
from services.user import (
    create_user,
    get_user_by_username,
    get_user_by_email,
    get_username_by_token,
)
from services.utils import send_to_connection
from services.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
)


async def create_user_handler(connection_id, data: UserCreate):
    logger.info(f"Creating user {data.username}")
    try:
        await create_user(data)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': 'register',
            'status': 'error',
            'body': 'Error creating user'
        }
        send_to_connection(connection_id, message)
        message_for_log = message['body'] + ' ' + error_info
        logger.info(message_for_log)
        raise e

    message = {
        'command': 'register',
        'status': 'success',
        'body': 'User registered',
    }
    send_to_connection(connection_id, message)


async def login_handler(connection_id, data: UserLogin):
    try:
        validate_email(data.username_or_email)
        user = await get_user_by_email(data.username_or_email)
    except EmailNotValidError:
        user = await get_user_by_username(data.username_or_email)

    if user is None:
        message = {
            'command': 'login',
            'status': 'error',
            'body': 'User not registered',
        }
        send_to_connection(connection_id, message)
        return

    if not verify_password(data.password, user.password):
        message = {
            'command': 'login',
            'status': 'error',
            'body': 'Incorrect email or password',
        }
        send_to_connection(connection_id, message)
        return

    message = {
        'command': 'login',
        'status': 'success',
        'body': {
            "access_token": create_access_token(user.username),
            "refresh_token": create_refresh_token(user.username),
        }
    }
    send_to_connection(connection_id, message)


async def read_user_handler(connection_id, data: Token):
    try:
        username = get_username_by_token(data.token, 'access_token')
        user = await get_user_by_username(username)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': 'read_user',
            'status': 'error',
            'body': 'Error reading user'
        }
        send_to_connection(connection_id, message)
        message_for_log = message['body'] + ' ' + error_info
        logger.info(message_for_log)
        raise e

    if user is None:
        message = {
            'command': 'read_user',
            'status': 'error',
            'body': 'User not authorization'
        }
        send_to_connection(connection_id, message)

    message = {
        'command': 'read_user',
        'status': 'success',
        'body': {
            'username': user.username,
            'email': user.email,
        },
    }
    send_to_connection(connection_id, message)


async def update_token_handler(connection_id, data: Token):
    try:
        username = get_username_by_token(data.token, 'refresh_token')
        user = await get_user_by_username(username)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': 'update_token',
            'status': 'error',
            'body': 'Error reading user'
        }
        send_to_connection(connection_id, message)
        message_for_log = message['body'] + ' ' + error_info
        logger.info(message_for_log)
        raise e

    if user is None:
        message = {
            'command': 'update_token',
            'status': 'error',
            'body': 'User not authorization'
        }
        send_to_connection(connection_id, message)

    message = {
        'command': 'update_token',
        'status': 'success',
        'body': {
            "access_token": create_access_token(user.username),
            "refresh_token": create_refresh_token(user.username),
        }
    }
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_handler('register', UserCreate, create_user_handler)
    dp.add_handler('login', UserLogin, login_handler)
    dp.add_handler('read_user', Token, read_user_handler)
    dp.add_handler('update_token', Token, update_token_handler)
