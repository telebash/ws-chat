import openai
import requests
from typing import Any
from settings import settings


class ChatGpt4Service:
    authorization = settings.OPENAI_TOKEN,

    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        return await self.make_request()

    def __init__(self, **kwargs) -> None:
        self._prompt = kwargs.get('prompt')
        self.stream = kwargs.get('stream', False)
        self.default_messages = [
                    {
                        "role": "user",
                        "content": self._prompt
                    }
                ]
        if kwargs.get('messages'):
            self.default_messages: list[dict[str, Any]] = kwargs.get('messages')

    async def make_request(self, **kwargs) -> Any:
        openai.api_key = self.authorization[0]
        response = await openai.ChatCompletion.acreate(
            **self._build_request_json(),
            stream=self.stream
            )
        if self.stream:
            return response
        return response["choices"][0]['message']['content']

    def _build_request_json(self) -> dict:
        data = {
                "model": "gpt-4",
                "messages": self.default_messages
        }
        return data

    def _parse_response_json(self, response_json: dict) -> Any:
        if response_json.get('error'):
            raise requests.HTTPError(response_json['error']['message'])
        content = response_json['choices'][0]['message']['content']
        return content
