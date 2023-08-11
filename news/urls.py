from django.urls import path

from .views import list

app_name = 'news'

urlpatterns = [
    path('', list, name='list')
]
