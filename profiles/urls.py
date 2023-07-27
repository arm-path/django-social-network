from django.urls import path

from .views import user_registration, user_login, user_detail, profile_change

app_name = 'profile'

urlpatterns = [
    path('', user_detail, name='detail'),
    path('change/', profile_change, name='change'),
    path('login/', user_login, name='login'),
    path('registration/', user_registration, name='registration')
]
