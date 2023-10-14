import traceback
from datetime import datetime
import aiohttp
from loguru import logger
from dateutil.relativedelta import relativedelta
import openai

from services import ChatPrompts, TextSize
from services.integrations.openai_chat_gpt import ChatGpt4Service
from services.integrations.stable_dif import (
    StabilityAIService,
    StabilityAIUpscale,
    ReplicateStableDiffusionService
)
from services.utils import send_to_connection, get_s3_image_bytes


async def get_content_plan_from_gpt(message, state, niche: str, posts_count: str) -> str:
    logger.info('Get content plan flow')
    date_prefix = get_date_prefix()
    prompt = ChatPrompts.CONTENT_PLAN.value.format(
        date_prefix=date_prefix,
        specialization=niche,
        posts_count=posts_count,
    )
    if posts_count == '1' or posts_count == 'один' or posts_count == 'Один':
        prompt = prompt.replace('поста', 'пост')
    logger.info(prompt)
    data = {
        'prompt': prompt
    }
    service = ChatGpt4Service(**data)
    try:
        content = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = 'Серверы нагружены. Попробуйте позднее'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = 'Произошла ошибка. Сообщите ее по команде /feedback'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    return content


async def get_themes_from_chat_gpt(connection_id, niche: str, post_type: str) -> list:
    logger.info('Get themes flow')
    date_prefix = get_date_prefix()
    prompt = ChatPrompts.POST_THEME.value.format(
        date_prefix=date_prefix,
        specialization=niche,
        post_type=post_type
    )
    logger.info(prompt)
    data = {
        'prompt': prompt
    }
    service = ChatGpt4Service(**data)
    try:
        content = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Серверы нагружены. Попробуйте позднее'
        }
        send_to_connection(connection_id, message_for_user)
        message_for_log = message_for_user['body'] + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Произошла ошибка. Сообщите ее по команде /feedback'
        }
        send_to_connection(connection_id, message_for_user)
        message_for_log = message_for_user['body'] + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        raise e
    _list = content.split('\n')
    return list(filter(lambda x: x != "", _list))


async def function_clarification(message, state, theme: str, niche_name: str) -> bool:
    logger.info('Clarification flow')
    prompt = ChatPrompts.CLARIFICATION_PROMPT.value.format(
        title=theme,
        niche_name=niche_name
    )
    logger.info(prompt)
    data = {
        "messages": [
            {
                "role": "system",
                "content": prompt
            }
        ]
    }
    service = ChatGpt4Service(**data)
    try:
        answer = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = 'Серверы нагружены. Попробуйте позднее'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = 'Произошла ошибка. Сообщите ее по команде /feedback'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    print(answer)
    if answer == 'Готово':
        return True
    return False


async def give_me_questions(message, state, theme: str, niche_name: str) -> list:
    logger.info('Questions flow')
    system_prompt = ChatPrompts.CLARIFICATION_PROMPT.value.format(
        title=theme,
        niche_name=niche_name
    )
    prompt = ChatPrompts.LIST_OF_QUESTIONS.value
    logger.info(prompt)
    data = {
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "assistant",
                "content": "У меня есть вопросы."
            },
            {
                "role": "system",
                "content": prompt
            }
        ]
    }
    service = ChatGpt4Service(**data)
    try:
        answer = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = 'Серверы нагружены. Попробуйте позднее'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = 'Произошла ошибка. Сообщите ее по команде /feedback'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    _list = answer.split('\n')
    return list(filter(lambda x: x != "", _list))


async def answer_the_question(message, state, theme: str, niche_name: str, answer: str, questions: str) -> str:
    system_prompt = ChatPrompts.CLARIFICATION_PROMPT.value.format(
        title=theme,
        niche_name=niche_name
    )
    prompt = ChatPrompts.LIST_OF_QUESTIONS.value
    data = {
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "assistant",
                "content": "У меня есть вопросы."
            },
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "assistant",
                "content": questions
            },
            {
                "role": "system",
                "content": answer
            },
        ]
    }
    logger.info(answer)
    service = ChatGpt4Service(**data)
    try:
        answer = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = 'Серверы нагружены. Попробуйте позднее'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = 'Произошла ошибка. Сообщите ее по команде /feedback'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    print(answer)
    return answer


async def get_post_from_chat_gpt(connection_id, theme: str, project: str, text_style, text_size='small') -> str:
    logger.info('Create Post flow')
    date_prefix = get_date_prefix()
    if text_size == 'big':
        text_size_prompt = 'Удели внимание деталям и обогати текст интересными фактами или историями.'
    else:
        text_size_prompt = 'Пиши кратко и лаконично.'
    prompt = ChatPrompts.CREATE_POST.value.format(
        date_prefix=date_prefix,
        theme=theme,
        specialization=project,
        text_style=text_style,
        text_size_prompt=text_size_prompt
    )
    logger.info(prompt)
    data = {
        'prompt': prompt,
        'stream': True
    }
    service = ChatGpt4Service(**data)
    try:
        content = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Серверы нагружены. Попробуйте позднее'
        }
        send_to_connection(connection_id, message_for_user)
        message_for_log = message_for_user['body'] + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Произошла ошибка. Сообщите ее по команде /feedback'
        }
        send_to_connection(connection_id, message_for_user)
        message_for_log = message_for_user['body'] + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        raise e
    return content


async def get_post_from_chat_gpt_with_questions(message, state, theme: str, niche: str, questions, answer, text_style) -> str:
    logger.info('Create Post with questions flow')
    date_prefix = get_date_prefix()
    data = await state.get_data()
    text_size = data.get('text_size')
    if text_size == TextSize.BIG_TEXT.value[-1]:
        text_size_prompt = 'Удели внимание деталям и обогати текст интересными фактами или историями.'
    else:
        text_size_prompt = 'Пиши кратко и лаконично.'
    prompt = ChatPrompts.CREATE_POST.value.format(
        date_prefix=date_prefix,
        theme=theme,
        specialization=niche,
        text_style=text_style,
        text_size_prompt=text_size_prompt
    )
    system_prompt = ChatPrompts.CLARIFICATION_PROMPT.value.format(
        title=theme,
        niche_name=niche
    )
    give_me_prompt = ChatPrompts.LIST_OF_QUESTIONS.value
    logger.info(prompt)
    data = {
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "assistant",
                "content": "У меня есть вопросы."
            },
            {
                "role": "system",
                "content": give_me_prompt
            },
            {
                "role": "assistant",
                "content": questions
            },
            {
                "role": "system",
                "content": answer
            },
            {
                "role": "assistant",
                "content": 'Готово'
            },
            {
                "role": "system",
                "content": prompt
            },
        ],
        'stream': True
    }
    service = ChatGpt4Service(**data)
    print(data)
    try:
        content = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = 'Серверы нагружены. Попробуйте позднее'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        await state.finish()
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = 'Произошла ошибка. Сообщите ее по команде /feedback'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        raise e
    logger.info(content)
    return content


async def get_prompt_for_sd_from_chat_gpt(connection_id, text: str) -> str:
    data = {
        'prompt': ChatPrompts.CREATE_PROMPT.value.format(text=text)
    }
    service = ChatGpt4Service(**data)
    try:
        content = await service()
    except openai.error.ServiceUnavailableError as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Серверы нагружены. Попробуйте позднее'
        }
        send_to_connection(connection_id, message_for_user)
        raise e
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Серверы нагружены. Попробуйте позднее'
        }
        send_to_connection(connection_id, message_for_user)
        raise e
    return content


async def get_image_from_stability(prompt: str, style: str = '', seed: int = 0, scale_data: str = '1024x1024'):
    width, height = scale_data.split('x')
    data = {
        'prompt': prompt,
        'width': int(width),
        'height': int(height),
        'style': style,
        'seed': seed
    }
    service = StabilityAIService(**data)
    return await service()


async def get_image_from_replicate(prompt: str, style: str = '', seed: int = 0, scale_data: str = '1024x1024'):
    width, height = scale_data.split('x')
    data = {
        'prompt': prompt,
        'width': int(width),
        'height': int(height),
        'style': style,
        'seed': seed
    }
    service = ReplicateStableDiffusionService(**data)
    return await service()


async def get_upscale_image_from_stable_diffusion(connection_id, image_name: str, scale_data: str = '1024x1024'):
    image = get_s3_image_bytes(connection_id, image_name)
    width, height = scale_data.split('x')
    data = {
        'image': image,
        'width': int(width),
        'height': int(height),
    }
    service = StabilityAIUpscale(**data)
    try:
        content, image_url = await service()
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Произошла ошибка. Сообщите ее по команде /feedback'
        }
        send_to_connection(connection_id, message_for_user)
        message_for_log = message_for_user['body'] + '\n' + error_info
        raise e
    return content, image_url


async def get_image_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.request("GET", url) as resp:
            r = await resp.read()
            return r


async def image_resolutions(
        message,
        provider: str,
        scale_data: str,
        prompt: str,
        style: str = '',
        seed: int = 0
):
    width, height = scale_data.split('x')
    data = {
        'prompt': prompt,
        'style': style,
        'width': int(width),
        'height': int(height),
        'seed': seed
    }
    if provider == 'replicate':
        service = ReplicateStableDiffusionService(**data)
    else:
        service = StabilityAIService(**data)
    try:
        content, image_url = await service()
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = 'Произошла ошибка. Сообщите ее по команде /feedback'
        await message.answer(message_for_user)
        message_for_log = message_for_user + '\n' + error_info
        # await log_message(message.chat.id, message_for_log, 'bot')
        raise e
    return content, image_url


# async def subscription_checker(message):
#     user = await get_user_by_telegram_id(message.chat.id)
#     if user.is_admin_user:
#         return user
#     if not user.paid:
#         return user
#     current_date = datetime.now()
#     subscription_date = user.subscription_date
#     payment = user.payments[0]
#     if payment.total_amount == 200000:
#         subscription_duration = relativedelta(days=1)
#     elif payment.total_amount == 1000000:
#         subscription_duration = relativedelta(days=7)
#     elif payment.total_amount == 2000000:
#         subscription_duration = relativedelta(months=1)
#     subscription_expiry_date = subscription_date + subscription_duration
#
#     if current_date > subscription_expiry_date:
#         await user.update(session=Session(), paid=False)
#
#     return user


# async def first_start_date_checker(message):
#     user = await get_user_by_telegram_id(message.chat.id)
#     if user.is_admin_user:
#         return user
#     current_date = datetime.now()
#     first_start_date = user.first_start_date
#     start_duration = relativedelta(days=7)
#     start_expiry_date = first_start_date + start_duration
#
#     if current_date > start_expiry_date:
#         await user.update(session=Session(), free_use_bool=False)
#         return None
#
#     return user


def get_date_prefix():
    import locale
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    return f"Сегодня {datetime.now().strftime('%d %B %Y года, %A')}"


def get_random_seed():
    import random
    import time
    random.seed(time.time())
    random_seed = random.randint(0, 4294967295)
    return random_seed
