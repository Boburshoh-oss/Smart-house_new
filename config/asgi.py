"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_project = get_asgi_application()


from channels.routing import ProtocolTypeRouter,URLRouter
from mysite.consumers import MyMqttConsumer
from channels.auth import AuthMiddlewareStack
import mysite.routing


application = ProtocolTypeRouter({
        'http': django_project,
        'mqtt': MyMqttConsumer.as_asgi(),  
        "websocket": AuthMiddlewareStack(
            URLRouter(
                mysite.routing.websocket_urlpatterns
            )
        ),
    })
