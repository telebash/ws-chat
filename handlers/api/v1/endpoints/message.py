from fastapi import APIRouter, Depends, HTTPException

from handlers.api.deps import get_current_user
from db.models.user import User
from schemas.message import SaveMessages
from services import ChatEnum
from services.message import get_messages, save_messages

router = APIRouter()


@router.get('/{project_id}/{chat}')
async def get_messages_router(
        project_id: int,
        chat: ChatEnum,
        skip: int = 0,
        limit: int = 100,
        user: User = Depends(get_current_user),
):
    try:
        messages = await get_messages(
            project_id=project_id,
            chat=chat,
            skip=skip,
            limit=limit,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error while getting messages')

    return {
        'data': messages,
    }


@router.post('/')
async def save_messages_router(data: SaveMessages, user: User = Depends(get_current_user),):
    try:
        await save_messages(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error saving messages')

    return {
        'message': 'Messages saved'
    }
