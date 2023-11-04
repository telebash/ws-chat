from typing import Callable, Any, Awaitable, TypedDict

from pydantic import BaseModel


class Handler(TypedDict):
    handler: Callable[[Any, Any], Awaitable[Any]]
    model: type[BaseModel]


class AsyncDispatcher:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}

    def add_handler(
            self,
            event_name: str,
            schema: type[BaseModel],
            handler: Callable[[Any, Any], Awaitable[Any]]
    ):
        self.handlers[event_name] = {
            'handler': handler,
            'model': schema,
        }

    def remove_handler(self, event_name):
        if event_name in self.handlers:
            del self.handlers[event_name]

    async def trigger_event(self, event_name: str, session_id: str, **kwargs):
        if event_name in self.handlers:
            listener = self.handlers[event_name]
            model = listener['model']
            data = model(**kwargs)
            handler = listener['handler']
            await handler(session_id, data)
        else:
            raise ValueError(f'No event {event_name} registered')
