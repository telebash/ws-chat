class Dispatcher:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def remove_listener(self, event_name, listener):
        if event_name in self.listeners:
            if listener in self.listeners[event_name]:
                self.listeners[event_name].remove(listener)

    def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(*args, **kwargs)


class AsyncDispatcher:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_name, listener):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def remove_listener(self, event_name, listener):
        if event_name in self.listeners:
            if listener in self.listeners[event_name]:
                self.listeners[event_name].remove(listener)

    async def trigger_event(self, event_name, *args, **kwargs):
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                await listener(*args, **kwargs)
