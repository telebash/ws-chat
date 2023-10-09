import json
import logging
import os

import boto3


def get_event_body(event) -> dict:
    try:
        body = json.loads(event.get("body", ""))
    except Exception as ex:
        logging.error(ex)
        raise Exception('Bad request body. It is not json')
    return body


def send_to_connection(connection_id, data):
    endpoint = os.environ['WEBSOCKET_API_ENDPOINT']
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint)
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data, ensure_ascii=False))
