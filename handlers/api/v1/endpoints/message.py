from loguru import logger
from fastapi import APIRouter, Depends, HTTPException

from handlers.api.deps import get_current_user
from db.models.user import User
from schemas.message import SaveMessages, SaveMessage
from services import ChatEnum
from services.message import get_messages, save_messages, save_message
from services.project import get_project

router = APIRouter()


@router.get('/{project_id}/{chat}')
async def get_messages_router(
        project_id: int,
        chat: ChatEnum,
        skip: int = 0,
        limit: int = 100,
        user: User = Depends(get_current_user),
):
    project = await get_project(project_id)

    if not project or project.user_id != user.id:
        raise HTTPException(status_code=403, detail='You are not allowed to access this project')

    messages = await get_messages(
        project_id=project_id,
        chat=chat,
        skip=skip,
        limit=limit,
    )
    return {
        'data': messages,
    }


@router.post('/')
async def save_messages_router(data: SaveMessages, user: User = Depends(get_current_user),):
    project = await get_project(data.project_id)

    if not project or project.user_id != user.id:
        raise HTTPException(status_code=403, detail='You are not allowed to access this project')

    try:
        await save_messages(data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Error saving messages')

    return {
        'message': 'Messages saved'
    }


@router.post('/one')
async def save_message_router(
        data: SaveMessage,
        user: User = Depends(get_current_user)
):
    project = await get_project(data.project_id)

    if not project or project.user_id != user.id:
        raise HTTPException(status_code=403, detail='You are not allowed to access this project')

    try:
        await save_message(data)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Error saving message')

    return {
        'message': 'Message saved'
    }
