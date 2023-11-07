from fastapi import APIRouter, Depends

from db.models.user import User
from handlers.api.deps import get_current_user

router = APIRouter()


@router.get('/me/')
async def read_user(user: User = Depends(get_current_user)):
    del user.password
    return {
        'data': user,
    }
