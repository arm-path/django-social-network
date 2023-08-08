from django.shortcuts import render, get_object_or_404

from profiles.models import User
from .models import Chat
from .services import create_chat


def detail(request, username):
    user = get_object_or_404(User, username=username)
    chat = Chat.objects.filter(users__in=[user.id]).filter(users__in=[request.user.id])
    chat = create_chat([request.user.id, user.id]) if not chat else chat[0]
    return render(request, 'chat/detail.html', {'messages': chat.messages.all(), 'user': user})


def list(request):
    pass_objects = []
    object_list = request.user.chats.all()
    return render(request, 'chat/list.html', {'object_list': object_list, 'pass_objects': pass_objects})
