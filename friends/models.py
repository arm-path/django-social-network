from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from profiles.models import User
from news.models import Action


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscription = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests')
    friends = models.BooleanField(default=False, help_text='Friend request confirmation')
    black_list = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.subscription}'

    class Meta:
        unique_together = ('user', 'subscription')
        verbose_name = 'firend'
        verbose_name_plural = 'friends'


@receiver(post_save, sender=Friend)
def create_action(sender, instance, created, **kwargs):
    if created:
        Action.objects.create(user=instance.user, verb=settings.ACTION_VERBS['subscribe'],
                              target_object=instance.subscription)
    if not created and instance.friends:
        Action.objects.create(user=instance.subscription, verb=settings.ACTION_VERBS['friend'],
                              target_object=instance.user)
        Action.objects.create(user=instance.user, verb=settings.ACTION_VERBS['friend'],
                              target_object=instance.subscription)
