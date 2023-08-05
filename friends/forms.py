from django import forms
from django.conf import settings

from profiles.models import User


class FriendForm(forms.Form):
    ACTION_CHOICES = (
        (settings.ACTIONS_USER['subscribe'], settings.ACTIONS_USER['subscribe']),
        (settings.ACTIONS_USER['cancel'], settings.ACTIONS_USER['cancel']),
        (settings.ACTIONS_USER['confirm'], settings.ACTIONS_USER['confirm']),
        (settings.ACTIONS_USER['remove'], settings.ACTIONS_USER['remove']),
        (settings.ACTIONS_USER['black_list'], settings.ACTIONS_USER['black_list'])
    )
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.HiddenInput())
