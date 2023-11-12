from loguru import logger

from dispatcher import AsyncDispatcher
from schemas.theme import CreateTheme
from services.auth import auth_check_and_get_user
from services.chat_gpt import get_themes_from_chat_gpt
from services.subscription import subscription_checker, user_trial_checker
from services.utils import send_to_connection


async def create_theme_handler(connection_id, data: CreateTheme):
    command = 'create_theme'
    user = await auth_check_and_get_user(connection_id, command, data.token)

    user = await subscription_checker(user)
    is_trial = user_trial_checker(user)
    if not is_trial and not user.paid:
        logger.info('User does not have subscription')
        message = {
            'command': command,
            'status': 'error',
            'body': 'Subscription expired'
        }
        send_to_connection(connection_id, message)
        return
    if not is_trial:
        logger.info('User has not free use')
        message = {
            'command': command,
            'status': 'error',
            'body': 'Trial expired'
        }
        send_to_connection(connection_id, message)
        return

    themes = await get_themes_from_chat_gpt(connection_id, data.project, data.text_style)
    message = {
        'type': 'themes',
        'body': themes,
    }
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_handler('create_theme', CreateTheme, create_theme_handler)
