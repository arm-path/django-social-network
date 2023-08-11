from django.contrib.auth.decorators import login_required
from django.db.models import Q, Case, When
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.conf import settings

from friends.models import Friend
from profiles.services import objects_page
from .models import Action


@login_required
@require_http_methods(['GET'])
def list(request):
    user_ids = Friend.objects.filter(Q(user=request.user) | Q(subscription=request.user, friends=True)).annotate(
        ids=Case(When(user=request.user, then='subscription_id'),
                 When(subscription=request.user, friends=True, then='user_id'))).values('ids')
    actions = Action.objects.filter(user__in=user_ids)
    object_list = objects_page(actions, settings.TATAL_NEW_PAGE, request.GET.get('page'))
    return render(request, 'news/list.html', {'object_list': object_list})
