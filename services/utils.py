import base64
import json
import logging
import traceback
import uuid
import boto3

from settings import settings


def get_event_body(event) -> dict:
    try:
        body = json.loads(event.get("body", ""))
    except Exception as ex:
        logging.error(ex)
        raise Exception('Bad request body. It is not json')
    return body


def get_event_auth_header(event) -> str:
    try:
        auth_header = event.get("headers", {}).get("Authorization", "")
    except Exception as ex:
        logging.error(ex)
        raise Exception('Bad request header. It is not json')
    return auth_header


def send_to_connection(connection_id, data):
    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=settings.WS_ENDPOINT)
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data, ensure_ascii=False))


def generate_image_name() -> str:
    return str(uuid.uuid4()) + '.png'


def upload_s3_image_base64(connection_id, image_name, image_base64: str) -> str:
    s3 = boto3.client('s3')
    bucket_name = settings.BUCKET_NAME

    image_bytes = base64.b64decode(image_base64.encode())

    try:
        s3.put_object(Body=image_bytes, Bucket=bucket_name, Key=image_name)
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Произошла ошибка.'
        }
        send_to_connection(connection_id, message_for_user)
        message_for_log = message_for_user['body'] + '\n' + error_info
        raise e

    return f'https://{bucket_name}.s3.amazonaws.com/{image_name}'


def get_s3_image_bytes(connection_id, image_name) -> bytes:
    s3 = boto3.client('s3')
    bucket_name = settings.BUCKET_NAME

    try:
        response = s3.get_object(Bucket=bucket_name, Key=image_name)
    except Exception as e:
        error_info = traceback.format_exc()
        message_for_user = {
            'type': 'error',
            'body': 'Произошла ошибка.'
        }
        send_to_connection(connection_id, message_for_user)
        message_for_log = message_for_user['body'] + '\n' + error_info
        raise e

    return response['Body'].read()
