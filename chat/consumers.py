import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.urls import reverse
from django.utils import timezone

from .services import MessageWebsocketConsumer


class ChatConsumer(MessageWebsocketConsumer, WebsocketConsumer):
    def connect(self):
        self.room_group_name = None
        self.check_websocket_connect()

    def disconnect(self, close_code):
        if self.room_group_name is not None:
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        self.text_data_json = json.loads(text_data)
        message = {
            'text': self.text_data_json['message'],
            'date': timezone.now().strftime('%d.%m.%Y %H:%M')
        }
        user = {'username': self.me.username,
                'full_name': self.me.get_full_name(),
                'url': reverse('profile:detail', args=[self.me.user_slug])}
        self.enter_data_into_database()
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,
                                                     {'type': 'chat_message',
                                                      'message': message,
                                                      'user': user})

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
