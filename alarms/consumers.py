from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import Alarm


# ------ view와 channels의 중간 다리 역할/request 처리

@receiver(post_save, sender=Alarm)
def announce_likes(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        # send 등 과 같은 동기적인 함수를 비동기적으로 사용하기 위해서는 async_to_sync 로 감싸줘야한다.
        # group: 그룹 이름을 가진 사용자는 누구나 그룹에 채널을 추가 / 삭제 가능하고 그룹의 모든 채널에게 메세지를 보낼 수 있습니다.
        async_to_sync(channel_layer.group_send)(
            # 그룹에 send
            # self.room_group_name = 'chat_%s' % self.room_name -> self.room_group_name 추가
            # todo 김유빈 그룹 정하기
            "shares", {
                "type": "share_message",
                "message": instance.message,
            }
        )


class UserTestConsumer(WebsocketConsumer):
    # ---새로운 클라이언트가 websocket을 통해 접속---
    # 해당 클라이언트가 해당 그룹에 들어왔다고 기록
    def connect(self):
        self.groupname = "shares"  # 공통된 그룹 이름
        self.accept()  # websocket에 연결

        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name,
        )

    # ---그룹에서 제거(클라이언트가 접속을 끊을 때)---
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.groupname,
            self.channel_name
        )

    # ---메세지 전달이 이루어지는 채널---
    # 해당 메세지는 같은 그룹안에 있는 다른 클라이언트들에게 브로캐스팅
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.groupname,
            {
                'type': 'share_message',
                'message': message
            }
        )

    # receive message from room group
    # alarms models에 데이터가 추가되면(버튼 누르면) 이 정보를 UserTestConsumer 에 있는 def share_message에 보냄
    # 보낸 정보(메세지)를 websocket이 연결된 페이지(alarm)에 보내는 논리
    def share_message(self, event):
        message = event['message']

        # send message to websocket
        self.send(text_data=json.dumps(
            {
                'message': message
            }
        ))
