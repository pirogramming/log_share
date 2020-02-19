from channels.routing import ProtocolTypeRouter, URLRouter
import alarms.routing

# 클라이언트와 Channels 개발 서버가 연결 될 때, 어느 protocol 타입의 연결인지
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 만약에 websocket protocol 이라면,
    'websocket': URLRouter(
        alarms.routing.websocket_urlpatterns
    )
})
