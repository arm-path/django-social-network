from django.shortcuts import redirect

from .forms import FriendForm
from .services import action_friend


def action(request):
    form = FriendForm(request.POST)
    if form.is_valid():
        action_friend(request.user, form.cleaned_data['user'])
    return redirect('profile:list')
