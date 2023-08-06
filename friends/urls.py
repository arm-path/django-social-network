from django.urls import path

from .views import action, friends, requests, subscriptions

app_name = 'friend'

urlpatterns = [
    path('', friends, name='friends'),
    path('requests/', requests, name='requests'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('action/<str:redirect_app_name>', action, name='action')
]
