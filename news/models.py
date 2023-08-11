from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from profiles.models import User


class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                    limit_choices_to={'model__in': ('user', 'friend', 'post')},
                                    related_name='target_actions')
    target_id = models.PositiveIntegerField()
    target_object = GenericForeignKey('target_type', 'target_id')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_full_name()} {self.verb} {self.target_object}'

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'
        indexes = [
            models.Index(fields=['target_type', 'target_id']),
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']
