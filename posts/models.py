from django.db import models
from django.urls import reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField

from profiles.models import User


class Post(models.Model):
    title = models.CharField(max_length=71)
    slug = models.SlugField(max_length=71, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} | {self.title}'

    def get_absolute_url(self):
        return reverse_lazy('post:detail', args=[self.user.user_slug, self.slug])

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [models.Index(fields=['id', 'slug']),
                   models.Index(fields=['title']),
                   models.Index(fields=['created'])]
