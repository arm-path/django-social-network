from django.conf import settings
from django.contrib.auth import authenticate, update_session_auth_hash, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.db.models import Q, Case, Count, When
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from posts.models import Post
from .forms import UserReistrationForm, UserLoginForm, ProfileChangeForm
from .models import User
from .services import objects_page, search_user, search_post, set_action_user


@require_http_methods(['GET', 'POST'])
def registration(request):
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


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user:
                auth_login(request, user)
                return redirect('profile:me')
            form.add_error('__all__', 'Login or password entered incorrectly!')

    if request.method == 'GET':
        form = UserLoginForm()
    return render(request, 'profiles/login.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def list(request):
    object_list = User.objects.annotate(
        is_request_user=Count(Case(When(friend_requests__user=request.user, friend_requests__friends=False, then=1))),
        is_subscribed=Count(Case(When(subscriptions__subscription=request.user, subscriptions__friends=False, then=1))),
        is_friend=Count(Case(When(Q(friend_requests__user=request.user, friend_requests__friends=True) |
                                  Q(subscriptions__subscription=request.user, subscriptions__friends=True), then=1))),
    ).exclude(username=request.user.username)
    if request.GET.get('search'):
        object_list = search_user(object_list, request.GET.get('search'))
    object_list = objects_page(object_list, settings.TOTAL_USER_PAGE, request.GET.get('page'))
    object_list = set_action_user(object_list)
    context = {'section': 'users', 'object_list': object_list}
    return render(request, 'profiles/list.html', context=context)


@login_required
@require_http_methods(['GET'])
def detail(request, user_slug=None):
    if user_slug:
        if request.user.user_slug == user_slug:
            return redirect('profile:me')
        user = get_object_or_404(User, user_slug=user_slug)
        object_list = Post.objects.filter(user=user)
    else:
        user = request.user
        object_list = Post.objects.filter(user=request.user)
    object_list = search_post(object_list, request.GET.get('search')) if request.GET.get('search') else object_list
    object_list = objects_page(object_list, settings.TOTAL_POST_PAGE, request.GET.get('page'))
    return render(request, 'profiles/detail.html', {'section': 'profile', 'user': user, 'object_list': object_list})


@login_required
@require_http_methods(['GET', 'POST'])
def edit(request):
    if request.method == 'POST':
        form = ProfileChangeForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile:me')
    if request.method == 'GET':
        form = ProfileChangeForm(instance=request.user)
    return render(request, 'profiles/edit.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile:me')
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {'form': form})


class ResetPassword(PasswordResetView):
    success_url = reverse_lazy('profile:password_reset_done')


class ConfirmResetPassword(PasswordResetConfirmView):
    success_url = reverse_lazy('profile:password_reset_compile')
