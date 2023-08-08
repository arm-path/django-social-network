from django.urls import path

from .views import detail, list

app_name = 'chat'

urlpatterns = [
    path('detail/<slug:username>/', detail, name='detail'),
    path('list/', list, name='list')
]
