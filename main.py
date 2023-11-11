import asyncio

from fastapi import FastAPI
from loguru import logger
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from dispatcher import AsyncDispatcher
from handlers.api.v1.api import api_router as api_v1
from handlers.ws import post, image, theme
# from handlers.ws import post, image, projects, message, theme, user
from services.utils import get_event_body
from core.config import settings

REQUEST_HANDLED = {"statusCode": 200}

dp = AsyncDispatcher()

post.register(dp)
image.register(dp)
theme.register(dp)
# user.register(dp)
# message.register(dp)
# projects.register(dp)

app = FastAPI(openapi_prefix='/default/')
mangum_handler = Mangum(app)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

app.include_router(api_v1, prefix=settings.API_V1_STR)

# @app.middleware("http")
# def add_process_time_header(request: Request, call_next):
#     print('request.url.path: ', request.url.path)
#     if 'default' not in request.url.path:
#         request.scope['path'] = '/default' + request.url.path
#         print('request.scope[path]: ', request.scope['path'])
#         print('middleware: url changed')
#     return call_next(request)


def connection_manager(event, context):
    if event["requestContext"]["eventType"] == "CONNECT":
        logger.info("Connect requested")
        return REQUEST_HANDLED
    elif event["requestContext"]["eventType"] == "DISCONNECT":
        logger.info("Disconnect requested")
        return REQUEST_HANDLED


async def handle_incoming_ws_message(event, context):
    logger.info("Handle incoming WS message")

    body = get_event_body(event)
    connection_id: str = event["requestContext"].get("connectionId")
    logger.info(connection_id)

    command = body["command"]
    data = body["data"]

    logger.info(command)
    logger.info(data)
    await dp.trigger_event(command, connection_id, **data)
    return REQUEST_HANDLED


def handler(event, context):
    route_key = event["requestContext"].get("routeKey", None)

    if route_key is None:
        return mangum_handler(event, context)

    if route_key == "$connect" or route_key == "$disconnect":
        connection_manager(event, context)
    elif route_key == "$default":
        return asyncio.get_event_loop().run_until_complete(handle_incoming_ws_message(event, context))
    else:
        return {"statusCode": 400}

    return REQUEST_HANDLED
