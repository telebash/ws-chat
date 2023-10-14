import traceback

from loguru import logger

from dispatcher import AsyncDispatcher
from services.chat_gpt import get_image_from_replicate, get_image_from_stability, \
    get_prompt_for_sd_from_chat_gpt, get_upscale_image_from_stable_diffusion
from services.utils import send_to_connection, upload_s3_image_base64, generate_image_name


async def create_image_handler(connection_id, text: str, style: str = '', scale_data: str = '1024x1024'):
    sd_prompt = await get_prompt_for_sd_from_chat_gpt(connection_id, text)
    logger.info(sd_prompt)
    image_base64, image_url = await get_image_from_replicate(sd_prompt, style=style, scale_data=scale_data)

    if not image_url:
        try:
            image_base64, image_url = await get_image_from_stability(sd_prompt, style=style, scale_data=scale_data)
        except Exception as e:
            error_info = traceback.format_exc()
            message_for_user = {
                'type': 'error',
                'body': 'Серверы нагружены. Попробуйте позднее'
            }
            send_to_connection(connection_id, message_for_user)
            message_for_log = message_for_user['body'] + '\n' + error_info
            raise e

    image_name = generate_image_name()
    image_url = upload_s3_image_base64(connection_id, image_name, image_base64)

    message = {
        'type': 'image',
        'body': image_url,
    }

    send_to_connection(connection_id, message)


async def upscale_image_handler(connection_id, image_name: str, scale_data: str = '1024x1024'):
    logger.info('Start Upscale Image')
    image_base64, image_url = await get_upscale_image_from_stable_diffusion(connection_id, image_name, scale_data)

    image_name = generate_image_name()
    image_url = upload_s3_image_base64(connection_id, image_name, image_base64)

    message = {
        'type': 'upscale_image',
        'body': image_url,
    }

    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_listener('create_image', create_image_handler)
    dp.add_listener('upscale_image', upscale_image_handler)
