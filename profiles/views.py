from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q, Case, When, CharField, Value
from django.conf import settings

from posts.models import Post
from friends.forms import FriendForm
from friends.models import Friend
from .forms import UserReistrationForm, UserLoginForm, ProfileChangeForm
from .models import User


def user_registration(request):
    if request.method == 'POST':
        form = UserReistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(email, username, password)

    if request.method == 'GET':
        form = UserReistrationForm()
    return render(request, 'profiles/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['login'].email
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('profile:me')
            form.add_error('__all__', 'Login or password entered incorrectly!')

    if request.method == 'GET':
        form = UserLoginForm()
    return render(request, 'profiles/login.html', {'form': form})


@login_required
def user_list(request):
    action = settings.ACTIONS_USER
    user = User.objects.annotate(
        action=Case(
            When(friend_requests__user=request.user, friend_requests__friends=True, then=Value(action['remove'])),
            When(subscriptions__subscription=request.user, subscriptions__friends=True,then=Value(action['remove'])),
            When(friend_requests__user=request.user, then=Value(action['cancel'])),
            When(subscriptions__subscription=request.user, then=Value(action['confirm'])),
            default=Value(action['subscribe']), output_field=CharField())).exclude(username=request.user.username)
    context = {'section': 'users', 'users': user}
    return render(request, 'profiles/list.html', context=context)


@login_required
def user_detail(request, user_slug=None):
    if user_slug:
        if request.user.user_slug == user_slug:
            return redirect('profile:me')
        user = get_object_or_404(User, user_slug=user_slug)
        posts = Post.objects.filter(user=user)
    else:
        user = request.user
        posts = Post.objects.filter(user=request.user)
    return render(request, 'profiles/detail.html', {'section': 'profile', 'user': user, 'posts': posts})


@login_required
def profile_change(request):
    if request.method == 'POST':
        form = ProfileChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile:detail')
    if request.method == 'GET':
        form = ProfileChangeForm(instance=request.user)
    return render(request, 'profiles/change.html', {'form': form})
