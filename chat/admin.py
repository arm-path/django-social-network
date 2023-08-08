from django.contrib import admin
from django.utils.html import mark_safe

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_users']

    def get_users(self, obj):
        users = obj.users.all()
        user_list = [f'<div>{user}</div>' for user in users]
        return mark_safe(''.join(user_list))

    get_users.short_description = 'users'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'recipient']
