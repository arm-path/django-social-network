from django.conf import settings
from django.db.models import Q

from profiles.services import objects_page, search_user
from .models import Friend


def action_friend(me, user):
    models_friend = Friend.objects.filter(Q(user=me, subscription=user) | Q(user=user, subscription=me))
    if models_friend:
        model_field = models_friend[0]
        if model_field.friends:
            model_field.delete()
        elif model_field.user == me:
            model_field.delete()
        elif model_field.subscription == me:
            model_field.friends = True
            model_field.save()
    else:
        Friend.objects.create(user=me, subscription=user)


def get_context(request, object_list, action):
    object_list = search_user(object_list, request.GET.get('search')) if request.GET.get('search') else object_list
    object_list = objects_page(object_list, settings.TOTAL_USER_PAGE, request.GET.get('page'))
    context = {'section': 'friends', 'action': settings.ACTIONS_USER[action], 'object_list': object_list}
    return context
