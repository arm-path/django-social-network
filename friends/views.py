from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from profiles.models import User
from .forms import FriendForm
from .services import action_friend, get_context


@login_required
def action(request, redirect_app_name):
    form = FriendForm(request.POST)
    print(request.POST)
    if form.is_valid():
        action_friend(request.user, form.cleaned_data['user'])
    if redirect_app_name == 'friend':
        return redirect('friend:friends')
    return redirect('profile:list')


@login_required
def friends(request):
    object_list = User.objects.filter(
        Q(friend_requests__user=request.user, friend_requests__friends=True) |
        Q(subscriptions__subscription=request.user, subscriptions__friends=True)
    ).exclude(username=request.user.username)
    context = get_context(request, object_list, 'remove')
    return render(request, 'friends/list.html', context=context)


def requests(request):
    object_list = User.objects.filter(
        subscriptions__subscription=request.user, subscriptions__friends=False
    ).exclude(username=request.user.username)
    context = get_context(request, object_list, 'confirm')
    return render(request, 'friends/list.html', context=context)


@login_required
def subscriptions(request):
    object_list = User.objects.filter(
        friend_requests__user=request.user, friend_requests__friends=False
    ).exclude(username=request.user.username)
    context = get_context(request, object_list, 'cancel')
    return render(request, 'friends/list.html', context=context)
