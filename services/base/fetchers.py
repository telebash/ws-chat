import requests
import aiohttp


class HTTPRequest:

    def __init__(
            self,
            url: str,
            headers: dict,
            method: str = 'POST',
            **kwargs
            ) -> None:
        self.url = url
        self.headers = headers
        self.method = method
        self.kwargs = kwargs

    async def make_request(self) -> requests.Response:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    self.method, self.url,
                    headers=self.headers, **self.kwargs) as resp:
                await resp.read()
            return resp
