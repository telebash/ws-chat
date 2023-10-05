import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from asgiref.compatibility import guarantee_single_callable
from mangum import Mangum

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

import chat.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
wrapped_application = guarantee_single_callable(application)
handler = Mangum(wrapped_application, lifespan="off")
