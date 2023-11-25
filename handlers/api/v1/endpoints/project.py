import math
import time

from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from handlers.api.deps import get_current_user
from db.models.user import User
from schemas.project import ProjectCreate
from services.project import (
    get_projects,
    create_project,
    get_project,
    delete_project,
    favourite_project,
    update_logo_project,
)
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
        if image.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(status_code=400, detail='Invalid file type')
        filename = f'logos/{math.floor(time.time())}_{image.filename}'
        image_url = upload_s3_file(filename, image.file)

    project = await create_project(user.id, data, image_url)

    return {
        'id': project.id,
        'message': 'Project created',
    }


@router.get('/{project_id}')
async def get_project_router(project_id: int, user: User = Depends(get_current_user)):
    project = await get_project(project_id)
    if not project or project.user_id != user.id:
        raise HTTPException(status_code=404, detail='Project not found or not your project')
    return {
        'data': project,
    }


@router.post('/{project_id}/favourite')
async def favourite_project_router(project_id: int, user: User = Depends(get_current_user)):
    is_favourite = await favourite_project(project_id, user.id)
    if not is_favourite:
        return {
            'message': 'The project has been removed from favorites',
        }
    return {
        'message': 'The project has been added to favorites',
    }


@router.post('/{project_id}/logo')
async def upload_logo_router(
        project_id: int,
        image: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    if image.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail='Invalid file type')
    filename = f'logos/{math.floor(time.time())}_{image.filename}'
    image_url = upload_s3_file(filename, image.file)
    await update_logo_project(project_id, user.id, image_url)
    return {
        'message': 'Project logo uploaded',
    }


@router.post('/{project_id}/delete')
async def delete_project_router(project_id: int, user: User = Depends(get_current_user)):
    is_deleted = await delete_project(project_id, user.id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail='Project not found or not your project')
    return {
        'message': 'Project deleted',
    }
