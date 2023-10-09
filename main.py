import asyncio

from loguru import logger

from dispatcher import AsyncDispatcher
from handlers import post, image
from services.utils import get_event_body

REQUEST_HANDLED = {"statusCode": 200}

dp = AsyncDispatcher()

post.register(dp)
image.register(dp)


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


def handler(event, context):
    route_key = event["requestContext"]["routeKey"]

    if route_key == "$connect" or route_key == "$disconnect":
        connection_manager(event, context)
    elif route_key == "$default":
        return asyncio.get_event_loop().run_until_complete(handle_incoming_ws_message(event, context))
    else:
        return {"statusCode": 400}

    return REQUEST_HANDLED
