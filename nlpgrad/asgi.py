"""
ASGI config for nlpgrad project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nlpgrad.settings')

django.setup()

from nlpgrad.routing import websocket_urlpatterns

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns())),
})