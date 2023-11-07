from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from handlers.api.deps import get_current_user
from db.models.user import User
from schemas.project import ProjectCreate
from services.project import get_projects, create_project
from services.utils import upload_s3_file

router = APIRouter()


@router.get('/')
async def get_projects_router(user: User = Depends(get_current_user)):
    try:
        projects = await get_projects(user_id=user.id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail='Error get projects')

    return {
        'data': projects,
    }


@router.post('/')
async def create_project_router(
        data: ProjectCreate = Depends(),
        image: UploadFile = File(default=None),
        user: User = Depends(get_current_user)
):
    image_url = None

    if image:
        filename = f'logos/{image.filename}'
        image_url = upload_s3_file(filename, image.file)

    try:
        await create_project(user.id, data, image_url)
    except Exception as e:
        logger.info(e)
        raise HTTPException(status_code=500, detail='Error create project')

    return {
        'message': 'Project created',
    }
