from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("ws/test/", consumers.ChatConsumer.as_asgi()),
]