from django.urls import path

from .views import user_registration, user_login
from .views import user_list, user_detail, profile_change

app_name = 'profile'

urlpatterns = [
    path('', user_detail, name='me'),
    path('user/<slug:user_slug>/', user_detail, name='detail'),
    path('users/', user_list, name='list'),
    path('change/', profile_change, name='change'),
    path('login/', user_login, name='login'),
    path('registration/', user_registration, name='registration')
]
