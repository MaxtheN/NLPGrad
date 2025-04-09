from django.urls import re_path

def websocket_urlpatterns():
    from chatbot.consumers import ChatConsumer
    return [
        re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
    ]