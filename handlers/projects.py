import traceback

from loguru import logger

from dispatcher import AsyncDispatcher
from schemas.project import ProjectCreate
from schemas.token import Token
from services.auth import auth_check_and_get_user
from services.project import get_projects, create_project
from services.utils import send_to_connection, jsonable_encoder


async def get_projects_handler(connection_id, data: Token):
    command = 'get_projects'
    user = await auth_check_and_get_user(connection_id, command, data.token)

    try:
        projects = await get_projects(user_id=user.id)
        projects = jsonable_encoder(projects)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': command,
            'status': 'error',
            'body': 'Error get projects'
        }
        send_to_connection(connection_id, message)
        message_for_log = message['body'] + ' ' + error_info
        logger.info(message_for_log)
        raise e

    message = {
        'command': command,
        'status': 'success',
        'body': {
            'projects': projects,
        },
    }
    send_to_connection(connection_id, message)


async def create_project_handler(connection_id, data: ProjectCreate):
    command = 'create_project'
    user = await auth_check_and_get_user(connection_id, command, data.token)

    try:
        await create_project(user.id, data)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': command,
            'status': 'error',
            'body': 'Error create project'
        }
        send_to_connection(connection_id, message)
        message_for_log = message['body'] + ' ' + error_info
        logger.info(message_for_log)
        raise e

    message = {
        'command': command,
        'status': 'success',
        'body': 'Ok',
    }
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_handler('get_projects', Token, get_projects_handler)
    dp.add_handler('create_project', ProjectCreate, create_project_handler)
