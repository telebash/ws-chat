from typing import Any

from dispatcher import AsyncDispatcher
from schemas.post import PostCreate
from services.auth import auth_check_and_get_user
from services.chat_gpt import get_post_from_chat_gpt
from services.post import create_post
from services.utils import send_to_connection


async def create_post_handler(connection_id: str, data: PostCreate):
    command = 'create_post'
    await auth_check_and_get_user(connection_id, command, data.token)

    response: Any = await get_post_from_chat_gpt(
        connection_id,
        data.theme,
        data.niche,
        data.text_style
    )
    message = {
        'command': command,
        'status': 'process',
        'body': '',
        'finish': False
    }
    update_count = 0

    async for r in response:
        message['body'] += r["choices"][0]['delta'].get('content', '')
        update_count += 1
        if update_count % 45 == 0:
            send_to_connection(connection_id, message)

    post_obj = await create_post(theme_text=data.theme, text=message['body'])
    message['post_id'] = post_obj.id
    message['status'] = 'success'
    message['finish'] = True
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_handler('create_post', PostCreate, create_post_handler)