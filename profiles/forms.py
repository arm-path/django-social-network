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

    def clean_login(self):
        login = self.cleaned_data['login']
        try:
            user = User.objects.get(Q(email=login) | Q(username=login))
            if not user.is_active:
                raise forms.ValidationError('This user is not active!')
        except User.DoesNotExist:
            raise forms.ValidationError('Specified user not found!')
        return user


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'date_of_birth', 'city']