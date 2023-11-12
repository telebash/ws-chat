import traceback

from loguru import logger

from dispatcher import AsyncDispatcher
from schemas.image import UpscaleImage, CreateImage
from services.auth import auth_check_and_get_user
from services.chat_gpt import (
    get_image_from_replicate, get_image_from_stability,
    get_prompt_for_sd_from_chat_gpt, get_upscale_image_from_stable_diffusion, get_random_seed,
)
from services.image import create_image
from services.subscription import subscription_checker, user_created_at_checker
from services.utils import send_to_connection, upload_s3_image_base64, generate_image_name


async def create_image_handler(connection_id, data: CreateImage):
    command = 'create_image'
    user = await auth_check_and_get_user(connection_id, command, data.token)

    user = await subscription_checker(user)
    if not await user_created_at_checker(user):
        logger.info('User has not free use')
        message = {
            'command': command,
            'status': 'error',
            'body': 'Trial expired'
        }
        send_to_connection(connection_id, message)
        return
    elif not user.paid:
        logger.info('User does not have subscription')
        message = {
            'command': command,
            'status': 'error',
            'body': 'Subscription expired'
        }
        send_to_connection(connection_id, message)
        return
    
    sd_prompt = await get_prompt_for_sd_from_chat_gpt(connection_id, data.text)
    logger.info(sd_prompt)
    seed = get_random_seed()
    image_base64, image_url = await get_image_from_replicate(
        sd_prompt,
        style=data.style,
        seed=seed,
        scale_data=data.scale_data
    )

    if not image_url:
        try:
            image_base64, image_url = await get_image_from_stability(
                sd_prompt,
                style=data.style,
                scale_data=data.scale_data
            )
        except Exception as e:
            error_info = traceback.format_exc()
            message_for_user = {
                'command': command,
                'status': 'error',
                'body': 'Серверы нагружены. Попробуйте позднее'
            }
            send_to_connection(connection_id, message_for_user)
            logger.error(error_info)
            raise e

    image_name = generate_image_name()
    image_url = upload_s3_image_base64(connection_id, image_name, image_base64)

    image_obj = await create_image(image_url, data.style, seed, sd_prompt)

    message = {
        'command': command,
        'status': 'success',
        'body': image_url,
        'image_id': image_obj.id
    }

    send_to_connection(connection_id, message)


async def upscale_image_handler(connection_id, data: UpscaleImage):
    logger.info('Start Upscale Image')
    command = 'upscale_image'
    user = await auth_check_and_get_user(connection_id, command, data.token)

    user = await subscription_checker(user)
    if not user.free_use_bool and not user.paid:
        logger.info('User does not have subscription')
        message = {
            'command': command,
            'status': 'error',
            'body': 'Subscription expired'
        }
        send_to_connection(connection_id, message)
        return
    elif user.free_use_bool and not await user_created_at_checker(user):
        logger.info('User has free use')
        message = {
            'command': command,
            'status': 'error',
            'body': 'Trial expired'
        }
        send_to_connection(connection_id, message)
        return
    
    image_base64, image_url = await get_upscale_image_from_stable_diffusion(
        connection_id,
        data.image_name,
        data.scale_data
    )

    image_name = generate_image_name()
    image_url = upload_s3_image_base64(connection_id, image_name, image_base64)

    message = {
        'command': command,
        'status': 'success',
        'body': image_url,
    }

    send_to_connection(connection_id, message)


def register(dp: AsyncDispatcher):
    dp.add_handler('create_image', CreateImage, create_image_handler)
    dp.add_handler('upscale_image', UpscaleImage, upscale_image_handler)
