from email_validator import validate_email, EmailNotValidError
from fastapi.security import HTTPAuthorizationCredentials
from loguru import logger
from fastapi import APIRouter, HTTPException, Security

from core.config import settings
from db.models.otp import OtpTypeEnum
from handlers.api.deps import security
from schemas.user import UserCreate, UserLogin, UserForgotPassword, UserNewPassword, UserVerifyEmail, UserSendVerify
from services.auth import verify_password, create_access_token, create_refresh_token, decode_refresh_token
from services.mail import send_email_async
from services.otp import generate_and_create_otp, delete_otp, get_otp_by_code
from services.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    delete_user,
    get_user,
    change_user_password,
    user_active,
)

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

    user = await create_user(data)
    otp = await generate_and_create_otp(user.id, OtpTypeEnum.VERIFY_EMAIL)
    url = f"{settings.DOMAIN}/verify-email?email={user.email}&otp={otp.code}"
    result = {
        'message': 'User created',
        'email': False
    }
    try:
        await send_email_async(
            'Email Verification',
            user.email,
            'email-verification',
            {'url': url}
        )
        result['email'] = True
    except Exception as e:
        logger.error(e)
        await delete_user(user.id)
        await delete_otp(otp.id)

    return result


@router.post('/sign-in')
async def sign_in(data: UserLogin):
    try:
        validate_email(data.username_or_email)
        user = await get_user_by_email(data.username_or_email)
    except EmailNotValidError:
        user = await get_user_by_username(data.username_or_email)

    if not user:
        raise HTTPException(status_code=400, detail="User not registered")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User not active")

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


@router.get('/refresh')
async def refresh(token: HTTPAuthorizationCredentials = Security(security)):
    try:
        username = decode_refresh_token(token.credentials)
    except Exception as e:
        if str(e) == "Token expired":
            raise HTTPException(status_code=401, detail="Token expired")
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await get_user_by_username(username)
    access_token = create_access_token(user.username)
    return {
        "access_token": access_token,
    }


@router.post('/forgot-password')
async def forgot_password_router(data: UserForgotPassword):
    user = await get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not registered")
    otp = await generate_and_create_otp(user.id, OtpTypeEnum.FORGOT_PASSWORD)
    url = f"{settings.DOMAIN}/new-password?email={user.email}&otp={otp.code}"
    try:
        await send_email_async(
            'Forgot password',
            user.email,
            'forgot-password',
            {'url': url}
        )
    except Exception as e:
        logger.error(e)
        await delete_otp(otp.id)
        raise HTTPException(status_code=500, detail="Could not send email. Please try again later")
    return {
        'message': 'Email sent',
    }


@router.post('/new-password')
async def new_password_router(data: UserNewPassword):
    otp = await get_otp_by_code(data.otp)
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid otp")
    if otp.type != OtpTypeEnum.FORGOT_PASSWORD:
        raise HTTPException(status_code=400, detail="Invalid otp")
    user = await get_user(otp.user_id)
    if user and user.email != data.email:
        raise HTTPException(status_code=400, detail="Invalid otp")
    await change_user_password(user.id, data.password)
    await delete_otp(otp.id)
    return {
        'message': 'Password changed',
    }


@router.post('/send-verify')
async def send_verify_router(data: UserSendVerify):
    user = await get_user_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not registered")
    otp = await generate_and_create_otp(user.id, OtpTypeEnum.VERIFY_EMAIL)
    url = f"{settings.DOMAIN}/verify-email?email={user.email}&otp={otp.code}"
    try:
        await send_email_async(
            'Email Verification',
            user.email,
            'email-verification',
            {'url': url}
        )
    except Exception as e:
        logger.error(e)
        await delete_otp(otp.id)
        raise HTTPException(status_code=500, detail="Could not send email. Please try again later")
    return {
        'message': 'Email sent',
    }


@router.post('/verify-email')
async def verify_email_router(data: UserVerifyEmail):
    otp = await get_otp_by_code(data.otp)
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid otp")
    if otp.type != OtpTypeEnum.VERIFY_EMAIL:
        raise HTTPException(status_code=400, detail="Invalid otp")
    user = await get_user(otp.user_id)
    if user and user.email != data.email:
        raise HTTPException(status_code=400, detail="Invalid otp")
    await user_active(user.id)
    await delete_otp(otp.id)
    return {
        'message': 'Email verified',
    }
