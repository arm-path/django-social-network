from django.contrib import admin

from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'verb', 'target_object', 'created')
    list_filter = ('created',)
