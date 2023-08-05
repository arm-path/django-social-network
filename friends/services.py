from django.db.models import Q

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
