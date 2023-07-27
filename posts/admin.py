from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created')
    list_filter = ('created',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
