from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify

from .forms import PostForm
from .models import Post


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.user = request.user
            post.save()
    if request.method == 'GET':
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})


def detail_post(request, user_slug, slug):
    post = get_object_or_404(Post, slug=slug, user__user_slug=user_slug)
    return render(request, 'posts/detail.html', {'post': post})
