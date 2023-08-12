from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from profiles.models import User
from friends.models import Friend
from .models import Chat
from .services import create_chat


@login_required
@require_http_methods(['GET'])
def detail(request, username):
    user = get_object_or_404(User, username=username)
    chat = Chat.objects.filter(users__in=[user.id]).filter(users__in=[request.user.id])
    chat = create_chat([request.user.id, user.id]) if not chat else chat[0]
    friends = Friend.objects.filter(Q(user=request.user, subscription=user, friends=True) |
                                    Q(user=user, subscription=request.user, friends=True))
    is_friends = True if friends else False
    return render(request, 'chat/detail.html', {'chat': chat, 'user': user, 'is_friends': is_friends})


@login_required
@require_http_methods(['GET'])
def list(request):
    object_list = request.user.chats.all()
    return render(request, 'chat/list.html', {'object_list': object_list})
