from django.contrib import admin

from .models import Friend


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'friends', 'black_list')
    list_editable = ('friends', 'black_list')
