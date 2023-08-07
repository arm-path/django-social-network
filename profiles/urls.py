from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView, LogoutView
from django.urls import path

from .views import ResetPassword, ConfirmResetPassword
from .views import list, detail, edit
from .views import registration, login, change_password

app_name = 'profile'

urlpatterns = [
    path('', detail, name='me'),
    path('user/<slug:user_slug>/', detail, name='detail'),
    path('users/', list, name='list'),
    path('change/', edit, name='edit'),
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', change_password, name='change_password'),

    path('password-reset/', ResetPassword.as_view(), name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', ConfirmResetPassword.as_view(), name='password_reset_confirm'),
    path('password-reset-compile/', PasswordResetCompleteView.as_view(), name='password_reset_complete')

]
