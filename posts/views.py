from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.text import slugify

from .forms import PostForm
from .models import Post


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.user = request.user
            post.save()
            return redirect(post.get_absolute_url())
    if request.method == 'GET':
        form = PostForm()
    return render(request, 'posts/create_edit.html', {'form': form, 'action': 'create'})


@login_required
@require_http_methods(['GET', 'POST'])
def edit(request, slug):
    post = get_object_or_404(Post, slug=slug, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect(post.get_absolute_url())
    if request.method == 'GET':
        form = PostForm(instance=post)
    return render(request, 'posts/create_edit.html', {'form': form, 'action': 'edit'})


def delete(request, slug):
    post = get_object_or_404(Post, slug=slug, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile:me')
    return render(request, 'posts/delete.html', {'post': post})


@login_required
@require_http_methods(['GET'])
def detail(request, user_slug, slug):
    post = get_object_or_404(Post, slug=slug, user__user_slug=user_slug)
    return render(request, 'posts/detail.html', {'post': post})
