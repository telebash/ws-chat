from dispatcher import AsyncDispatcher
from services.chat_gpt import get_post_from_chat_gpt
from services.utils import send_to_connection


async def create_post(connection_id, theme, project, text_style):
    response = await get_post_from_chat_gpt(
        connection_id,
        theme,
        project,
        text_style
    )
    message = {
        'type': 'post',
        'body': response
    }
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_listener('create_post', create_post)
