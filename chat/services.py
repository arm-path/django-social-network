from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from django.db.models import Q

from profiles.models import User
from friends.models import Friend
from .models import Chat, Message


def create_chat(users):
    if len(users) != 2:
        raise ValueError(f'create_chat() takes exactly two argument ({self.users})')
    chat = Chat.objects.create()
    chat.users.set(users)
    chat.save()
    return chat


class MessageWebsocketConsumer:
    def check_websocket_connect(self):
        try:
            self.me = self.scope['user']
            try:
                self.user = User.objects.get(user_slug=self.scope['url_route']['kwargs']['username'])
            except User.DoesNotExist:
                raise StopConsumer()
            self.chats = Chat.objects.filter(users__in=[self.me]).filter(users__in=[self.user])
            self.chat_id = self.scope['url_route']['kwargs']['chat_id']
            if not self.chats or self.chats[0].id != int(self.chat_id):
                raise StopConsumer()
            if not Friend.objects.filter(Q(user=self.me, subscription=self.user, friends=True) |
                                         Q(user=self.user, subscription=self.me, friends=True)):
                raise StopConsumer()
        except KeyError:
            raise StopConsumer()

        self.room_group_name = f'chat_{self.chat_id}'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def enter_data_into_database(self):
        message = Message(chat=self.chats[0],
                          sender=self.me, recipient=self.user,
                          text=self.text_data_json['message'])
        message.save()
        message.visibility.set([self.me.id, self.user.id])
