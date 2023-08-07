from django.urls import path

from .views import create, edit, delete, detail

app_name = 'posts'

urlpatterns = [
    path('create/', create, name='create'),
    path('edit/<slug:slug>/', edit, name='edit'),
    path('delete/<slug:slug>/', delete, name='delete'),
    path('detail/<slug:user_slug>/title/<slug:slug>/', detail, name='detail')
]
