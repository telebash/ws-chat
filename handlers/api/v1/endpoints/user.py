import io
import math
import time

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from db.models.user import User
from handlers.api.deps import get_current_user
from schemas.user import UserChangePassword
from services.auth import verify_password
from services.user import change_user_password, update_avatar_user
from services.utils import upload_s3_file

router = APIRouter()


@router.get('/me/')
async def read_user_router(user: User = Depends(get_current_user)):
    del user.password
    return {
        'data': user,
    }


@router.post('/upload-avatar')
async def upload_avatar_router(
        image: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    if image.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail='Invalid file type')
    filename = f'avatars/{math.floor(time.time())}_{image.filename}'
    image_url = upload_s3_file(filename, image.file)
    await update_avatar_user(user.id, image_url)
    return {
        'message': 'Avatar changed successfully',
    }


@router.post('/change-password')
async def change_user_password_router(data: UserChangePassword, user: User = Depends(get_current_user)):
    if not verify_password(data.old_password, user.password):
        raise HTTPException(status_code=400, detail='Incorrect password')
    await change_user_password(user.id, data.new_password)
    return {
        'message': 'Password changed successfully',
    }
