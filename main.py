import os
import json

import boto3

REQUEST_HANDLED = {"statusCode": 200}


def connection_manager(event, context):
    if event["requestContext"]["eventType"] == "CONNECT":
        print("Connect requested")
        return REQUEST_HANDLED
    elif event["requestContext"]["eventType"] == "DISCONNECT":
        print("Disconnect requested")
        return REQUEST_HANDLED


def send_ws_message(connection_id, body):
    if not isinstance(body, str):
        body = json.dumps(body)
    _send_to_connection(connection_id, body)


def _get_event_body(event):
    return {"message": event.get("body", "")}


def _send_to_connection(connection_id, data):
    endpoint = os.environ['WEBSOCKET_API_ENDPOINT']
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint)
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=data.encode('utf-8'))


def handle_incoming_ws_message(event, context):
    body = _get_event_body(event)
    body['type'] = 'echoReply'
    connection_id = event["requestContext"].get("connectionId")
    send_ws_message(connection_id, body)


def handler(event, context):
    route_key = event["requestContext"]["routeKey"]

    if route_key == "$connect" or route_key == "$disconnect":
        connection_manager(event, context)
    elif route_key == "$default":
        handle_incoming_ws_message(event, context)
    else:
        return {"statusCode": 400}

    return REQUEST_HANDLED
