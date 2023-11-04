import base64
import dataclasses
import json
import logging
import traceback
import uuid
from collections import deque, defaultdict
import datetime
from enum import Enum
from ipaddress import IPv4Address, IPv4Interface, IPv4Network, IPv6Address, IPv6Interface, IPv6Network
from pathlib import PurePath, Path
from re import Pattern
from types import GeneratorType
from typing import Any, Dict, List, Literal, Callable, Type, Union, Tuple
from decimal import Decimal
from pydantic import BaseModel, NameEmail, SecretBytes, SecretStr, AnyUrl
from pydantic.color import Color
from pydantic.version import VERSION as PYDANTIC_VERSION
import boto3
from pydantic_core import Url

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


def isoformat(o: Union[datetime.date, datetime.time]) -> str:
    return o.isoformat()


def decimal_encoder(dec_value: Decimal) -> Union[int, float]:
    """
    Encodes a Decimal as int of there's no exponent, otherwise float

    This is useful when we use ConstrainedDecimal to represent Numeric(x,0)
    where a integer (but not int typed) is used. Encoding this as a float
    results in failed round-tripping between encode and parse.
    Our Id type is a prime example of this.

    >>> decimal_encoder(Decimal("1.0"))
    1.0

    >>> decimal_encoder(Decimal("1"))
    1
    """
    if dec_value.as_tuple().exponent >= 0:  # type: ignore[operator]
        return int(dec_value)
    else:
        return float(dec_value)


ENCODERS_BY_TYPE: Dict[Type[Any], Callable[[Any], Any]] = {
    bytes: lambda o: o.decode(),
    Color: str,
    datetime.date: isoformat,
    datetime.datetime: isoformat,
    datetime.time: isoformat,
    datetime.timedelta: lambda td: td.total_seconds(),
    Decimal: decimal_encoder,
    Enum: lambda o: o.value,
    frozenset: list,
    deque: list,
    GeneratorType: list,
    IPv4Address: str,
    IPv4Interface: str,
    IPv4Network: str,
    IPv6Address: str,
    IPv6Interface: str,
    IPv6Network: str,
    NameEmail: str,
    Path: str,
    Pattern: lambda o: o.pattern,
    SecretBytes: str,
    SecretStr: str,
    set: list,
    uuid.UUID: str,
    Url: str,
    AnyUrl: str,
}


def _model_dump(
        model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    return model.model_dump(mode=mode, **kwargs)


def generate_encoders_by_class_tuples(
    type_encoder_map: Dict[Any, Callable[[Any], Any]]
) -> Dict[Callable[[Any], Any], Tuple[Any, ...]]:
    encoders_by_class_tuples: Dict[Callable[[Any], Any], Tuple[Any, ...]] = defaultdict(
        tuple
    )
    for type_, encoder in type_encoder_map.items():
        encoders_by_class_tuples[encoder] += (type_,)
    return encoders_by_class_tuples


encoders_by_class_tuples = generate_encoders_by_class_tuples(ENCODERS_BY_TYPE)


def jsonable_encoder(
        obj,
        include=None,
        exclude=None,
        by_alias=True,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        custom_encoder=None,
        sqlalchemy_safe=True,
) -> Any:
    """
    Convert any object to something that can be encoded in JSON.

    This is used internally by FastAPI to make sure anything you return can be
    encoded as JSON before it is sent to the client.

    You can also use it yourself, for example to convert objects before saving them
    in a database that supports only JSON.

    Read more about it in the
    [FastAPI docs for JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/).
    """
    custom_encoder = custom_encoder or {}
    if custom_encoder:
        if type(obj) in custom_encoder:
            return custom_encoder[type(obj)](obj)
        else:
            for encoder_type, encoder_instance in custom_encoder.items():
                if isinstance(obj, encoder_type):
                    return encoder_instance(obj)
    if include is not None and not isinstance(include, (set, dict)):
        include = set(include)
    if exclude is not None and not isinstance(exclude, (set, dict)):
        exclude = set(exclude)
    if isinstance(obj, BaseModel):
        # TODO: remove when deprecating Pydantic v1
        encoders: Dict[Any, Any] = {}
        if not PYDANTIC_VERSION.startswith("2."):
            encoders = getattr(obj.__config__, "json_encoders", {})  # type: ignore[attr-defined]
            if custom_encoder:
                encoders.update(custom_encoder)
        obj_dict = _model_dump(
            obj,
            mode="json",
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        if "__root__" in obj_dict:
            obj_dict = obj_dict["__root__"]
        return jsonable_encoder(
            obj_dict,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            # TODO: remove when deprecating Pydantic v1
            custom_encoder=encoders,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if dataclasses.is_dataclass(obj):
        obj_dict = dataclasses.asdict(obj)
        return jsonable_encoder(
            obj_dict,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            custom_encoder=custom_encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, dict):
        encoded_dict = {}
        allowed_keys = set(obj.keys())
        if include is not None:
            allowed_keys &= set(include)
        if exclude is not None:
            allowed_keys -= set(exclude)
        for key, value in obj.items():
            if (
                    (
                            not sqlalchemy_safe
                            or (not isinstance(key, str))
                            or (not key.startswith("_sa"))
                    )
                    and (value is not None or not exclude_none)
                    and key in allowed_keys
            ):
                encoded_key = jsonable_encoder(
                    key,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = jsonable_encoder(
                    value,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple, deque)):
        encoded_list = []
        for item in obj:
            encoded_list.append(
                jsonable_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list

    if type(obj) in ENCODERS_BY_TYPE:
        return ENCODERS_BY_TYPE[type(obj)](obj)
    for encoder, classes_tuple in encoders_by_class_tuples.items():
        if isinstance(obj, classes_tuple):
            return encoder(obj)

    try:
        data = dict(obj)
    except Exception as e:
        errors: List[Exception] = []
        errors.append(e)
        try:
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors) from e
    return jsonable_encoder(
        data,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )
