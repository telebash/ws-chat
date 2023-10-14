from dispatcher import AsyncDispatcher
from services.chat_gpt import get_themes_from_chat_gpt
from services.utils import send_to_connection


async def create_theme_handler(connection_id, project, text_style):
    themes = await get_themes_from_chat_gpt(connection_id, project, text_style)
    message = {
        'type': 'themes',
        'body': themes,
    }
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_listener('create_theme', create_theme_handler)
