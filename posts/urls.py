from django.urls import path

from .views import create_post, detail_post

app_name = 'posts'

urlpatterns = [
    path('create/', create_post, name='create'),
    path('detail/<slug:user_slug>/title/<slug:slug>/', detail_post, name='detail')
]
