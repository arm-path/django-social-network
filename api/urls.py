from django.urls import path

from .views import UserListAPIView, UserDetailAPIView, PostDetailAPIView

app_name = 'api'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='list'),
    path('user/<slug:user_slug>', UserDetailAPIView.as_view(), name='detail'),
    path('post/<slug:slug>/', PostDetailAPIView.as_view(), name='post_detail')
]
