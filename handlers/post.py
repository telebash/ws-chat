from typing import Any

from dispatcher import AsyncDispatcher
from services.chat_gpt import get_post_from_chat_gpt
from services.utils import send_to_connection


async def create_post_handler(connection_id, theme, project, text_style):
    response: Any = await get_post_from_chat_gpt(
        connection_id,
        theme,
        project,
        text_style
    )
    message = {
        'type': 'post',
        'body': '',
        'finish': False
    }
    update_count = 0

    async for r in response:
        message['body'] += r["choices"][0]['delta'].get('content', '')
        update_count += 1
        if update_count % 45 == 0:
            send_to_connection(connection_id, message)

    message['finish'] = True
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_listener('create_post', create_post_handler)
