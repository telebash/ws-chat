from email_validator import validate_email, EmailNotValidError
from fastapi.security import HTTPAuthorizationCredentials
from loguru import logger
from fastapi import APIRouter, HTTPException, Security

from handlers.api.deps import security
from schemas.user import UserCreate, UserLogin
from services.auth import verify_password, create_access_token, create_refresh_token, decode_refresh_token
from services.user import create_user, get_user_by_email, get_user_by_username

router = APIRouter()


@router.post('/sign-up', status_code=201)
async def sign_up(data: UserCreate):
    logger.info(f"Creating user {data.email}")

    user = await get_user_by_email(data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await get_user_by_username(data.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    await create_user(data)

    return {
        'message': 'User created',
    }


@router.post('/sign-in', status_code=200)
async def sign_in(data: UserLogin):
    try:
        validate_email(data.username_or_email)
        user = await get_user_by_email(data.username_or_email)
    except EmailNotValidError:
        user = await get_user_by_username(data.username_or_email)

    if not user:
        raise HTTPException(status_code=400, detail="User not registered")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)

    del user.password

    return {
        "data": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.get('/refresh', status_code=200)
async def refresh(token: HTTPAuthorizationCredentials = Security(security)):
    username = decode_refresh_token(token.credentials)
    user = await get_user_by_username(username)
    access_token = create_access_token(user.username)
    return {
        "access_token": access_token,
    }
