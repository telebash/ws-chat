import traceback

from loguru import logger

from dispatcher import AsyncDispatcher
from schemas.message import GetMessages, SaveMessages, SaveMessage
from services.auth import auth_check_and_get_user
from services.message import get_messages, save_messages, save_message
from services.utils import send_to_connection, jsonable_encoder


async def get_messages_handler(connection_id: str, data: GetMessages):
    command = 'get_messages'
    await auth_check_and_get_user(connection_id, command, data.token)

    try:
        messages = await get_messages(
            project_id=data.project_id,
            chat=data.chat,
            skip=data.skip,
            limit=data.limit,
        )
        messages = jsonable_encoder(messages)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': command,
            'status': 'error',
            'body': 'Error get messages'
        }
        send_to_connection(connection_id, message)
        message_for_log = message['body'] + ' ' + error_info
        logger.info(message_for_log)
        raise e

    message = {
        'command': command,
        'status': 'success',
        'body': {
            'messages': messages,
        },
    }
    send_to_connection(connection_id, message)


async def save_messages_handler(connection_id: str, data: SaveMessages):
    command = 'save_messages'
    await auth_check_and_get_user(connection_id, command, data.token)

    try:
        await save_messages(data.messages)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': command,
            'status': 'error',
            'body': 'Error save messages'
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


async def save_message_handler(connection_id: str, data: SaveMessage):
    command = 'save_messages'
    await auth_check_and_get_user(connection_id, command, data.token)

    try:
        await save_message(data)
    except Exception as e:
        error_info = traceback.format_exc()
        message = {
            'command': command,
            'status': 'error',
            'body': 'Error save message'
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
    dp.add_handler('get_messages', GetMessages, get_messages_handler)
    dp.add_handler('save_messages', SaveMessages, save_messages_handler)
    dp.add_handler('save_message', SaveMessage, save_message_handler)
