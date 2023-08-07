from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.utils.text import gettext_lazy as _

from .models import User


class UserReistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserLoginForm(forms.Form):
    login = forms.CharField(label=_('login'), widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput())


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'date_of_birth', 'city']