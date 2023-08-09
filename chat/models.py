from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import User


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='chats', validators=[MinValueValidator(2), MaxValueValidator(2)])

    def __str__(self):
        return f'Chat number {self.pk}: {[user.get_full_name() for user in self.users.all()]}'

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming')
    visibility = models.ManyToManyField(User, related_name='user_messages', blank=True)
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message number {self.pk}: {self.sender.username}'

    def save(self, *args, **kwargs):
        if not (self.sender in self.chat.users.all() and self.recipient in self.chat.users.all()):
            raise ValidationError('The sender and recipient are not part of the selected chat')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created']


@receiver(post_save, sender=Message)
def get_visibility(sender, instance, created, **kwargs):
    if created:
        instance.visibility.set([instance.sender.id, instance.recipient.id])
