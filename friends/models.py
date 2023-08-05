from django.db import models

from profiles.models import User


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
