from django.db import models
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_delete
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

from profiles.models import User
from news.models import Action


class Post(models.Model):
    title = models.CharField(max_length=71)
    slug = models.SlugField(max_length=71, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = RichTextUploadingField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('post:detail', args=[self.user.user_slug, self.slug])

    def get_api_url(self):
        return reverse_lazy('api:post_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [models.Index(fields=['id', 'slug']),
                   models.Index(fields=['title']),
                   models.Index(fields=['created'])]


@receiver(post_save, sender=Post)
def create_action(sender, instance, created, **kwargs):
    if created:
        Action.objects.create(user=instance.user, verb=settings.ACTION_VERBS['create_post'], target_object=instance)


@receiver(pre_delete, sender=Post)
def delete_action(sender, instance=Post, **kwargs):
    Action.objects.get(user=instance.user, verb=settings.ACTION_VERBS['create_post'],
                       target_type__model='post', target_id=instance.id).delete()
