import os
import json
import logging

import boto3

REQUEST_HANDLED = {"statusCode": 200}


def connection_manager(event, context):
    if event["requestContext"]["eventType"] == "CONNECT":
        logging.info("Connect requested")
        return REQUEST_HANDLED
    elif event["requestContext"]["eventType"] == "DISCONNECT":
        logging.info("Disconnect requested")
        return REQUEST_HANDLED


def _get_event_body(event) -> dict:
    try:
        body = json.loads(event.get("body", ""))
    except Exception as ex:
        logging.error(ex)
        raise Exception('Bad request body. It is not json')
    return body


def _send_to_connection(connection_id, data):
    endpoint = os.environ['WEBSOCKET_API_ENDPOINT']
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint)
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=data.encode('utf-8'))


def handle_incoming_ws_message(event, context):
    logging.info("Handle incoming WS message")

    body = _get_event_body(event)
    connection_id: str = event["requestContext"].get("connectionId")
    logging.info(connection_id)

    command = body["command"]
    logging.info(command)

    if command == "hi":
        _send_to_connection(connection_id, "Hello World!")
    else:
        _send_to_connection(connection_id, "Idk this command")


def handler(event, context):
    route_key = event["requestContext"]["routeKey"]

    if route_key == "$connect" or route_key == "$disconnect":
        connection_manager(event, context)
    elif route_key == "$default":
        handle_incoming_ws_message(event, context)
    else:
        return {"statusCode": 400}

    return REQUEST_HANDLED
