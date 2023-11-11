from dispatcher import AsyncDispatcher
from schemas.theme import CreateTheme
from services.chat_gpt import get_themes_from_chat_gpt
from services.utils import send_to_connection


async def create_theme_handler(connection_id, data: CreateTheme):
    themes = await get_themes_from_chat_gpt(connection_id, data.niche, data.text_style)
    message = {
        'type': 'themes',
        'body': themes,
    }
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_handler('create_theme', CreateTheme, create_theme_handler)
