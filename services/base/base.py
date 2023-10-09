import json
import backoff
from loguru import logger
import asyncio
import requests
from abc import ABC
from typing import Any

from services.base.fetchers import HTTPRequest


async def retry_sleep(details):
    logger.error("Retrying 10 seconds")
    await asyncio.sleep(10)


class BaseService(ABC):
    """
        A basic service that saves logs and makes requests to a given host and endpoint.

         >>> Parameters:
            -db (AsyncSession) : The database session to be used for logging.
            -logger_class (Logger) : The logger class to be used for logging.
            -json (dict) : A dict containing the data to be passed with the aiohttp.request.
            -request_class (HTTPRequest) : The request class to be used for making requests.
            -**kwargs : Any additional keyword arguments to be passed to the aiohttp.request class (auth,params).

        >>> Returns:
            - any : The response from the request.

        >>> Errors:
            - InvalidUrl : if the url is invalid
            - ConnectionError : if the service is unable to establish a connection with the host
            - HTTPError : if the response status code is not 200
        """
    method = 'POST'
    host: str
    endpoint: str
    timeout: int
    headers = {
        'accept': 'application/json'
    }

    def __init__(self, *,
                 request_class=HTTPRequest,
                 **kwargs) -> None:
        self.__pre_init__(**kwargs)
        data = self._build_request_json()
        url = self.host + self.endpoint
        self.request_class = request_class(
            method=self.method,
            url=url,
            headers=self.headers,
            **data,
        )

    def __pre_init__(self, **kwargs) -> None:
        pass

    def _build_request_json(self) -> dict:
        return {}

    @backoff.on_exception(backoff.expo, (requests.exceptions.HTTPError, asyncio.TimeoutError), max_tries=3, on_backoff=retry_sleep)
    async def makes_request(self):
        response = await self.request_class.make_request()
        self.response = response
        return await self._parse_response()

    async def __call__(self, *args, **kwargs) -> Any:
        return await self.makes_request()

    def _parse_response_json(self, response_json) -> Any:
        pass

    async def _parse_response(self) -> Any:
        if self.response.ok:
            # await self.save_cache(response_data)
            return self._parse_response_json(await self.response.json())
        else:
            text = await self.response.text()
            logger.error(f"Error in {self.__class__.__name__} status code {self.response.status}: {text}")
            raise requests.exceptions.HTTPError(text)

    async def handle_400_exception(self):
        text = await self.response.text()
        raise requests.exceptions.HTTPError(text)

    async def handle_500_exception(self):
        await self.handle_400_exception()

    def prepare_cache_data(self, data: str) -> dict:
        return json.loads(data)
