from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q

from posts.models import Post
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
                return redirect('profile:detail')
            form.add_error('__all__', 'Login or password entered incorrectly!')

    if request.method == 'GET':
        form = UserLoginForm()
    return render(request, 'profiles/login.html', {'form': form})


def user_list(request):
    users = User.objects.all()
    return render(request, 'profiles/list.html', {'section': 'users',
                                                  'users': users})


@login_required
def user_detail(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'profiles/detail.html', {'section': 'profile', 'posts': posts})


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
