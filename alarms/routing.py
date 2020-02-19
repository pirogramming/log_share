from . import consumers
from django.urls import re_path

#라우팅: django의 url 과 유사
websocket_urlpatterns = [
    re_path(r'ws/test/(?P<username>.*)/', consumers.UserTestConsumer),
]
