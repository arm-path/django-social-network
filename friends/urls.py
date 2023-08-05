from django.urls import path

from .views import action

app_name = 'friend'

urlpatterns = [
    path('', action, name='add')
]
