import traceback

from loguru import logger

from dispatcher import AsyncDispatcher
from services.chat_gpt import get_post_from_chat_gpt, get_image_from_replicate, get_image_from_stability, \
    get_prompt_for_sd_from_chat_gpt, get_upscale_image_from_stable_diffusion
from services.utils import send_to_connection


async def create_image(connection_id, text: str, style: str = '', scale_data: str = '1024x1024'):
    sd_prompt = await get_prompt_for_sd_from_chat_gpt(connection_id, text)
    logger.info(sd_prompt)
    post_image, image_url = await get_image_from_replicate(sd_prompt, style=style, scale_data=scale_data)
    if not image_url:
        try:
            post_image, image_url = await get_image_from_stability(sd_prompt, style=style, scale_data=scale_data)
        except Exception as e:
            error_info = traceback.format_exc()
            message_for_user = {
                'type': 'error',
                'body': 'Серверы нагружены. Попробуйте позднее'
            }
            send_to_connection(connection_id, message_for_user)
            message_for_log = message_for_user['body'] + '\n' + error_info
            raise e
    message = {
        'type': 'image',
        'body': post_image,
    }
    send_to_connection(connection_id, message)


async def upscale_image(connection_id, url: str, scale_data: str = '1024x1024'):
    post_image, image_url = await get_upscale_image_from_stable_diffusion(connection_id, url, scale_data)
    message = {
        'type': 'upscale_image',
        'body': post_image,
    }
    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_listener('create_image', create_image)
    dp.add_listener('upscale_image', upscale_image)
