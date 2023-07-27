from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.text import gettext_lazy as _
from django.utils.html import mark_safe
from django.conf.urls.static import static

from .models import User


@admin.register(User)
class ProfileAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 'get_image')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('get_image_detail',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'image', 'get_image_detail', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',), },),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'username', 'password1', 'password2'), },),)

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<image width="70px" src="{obj.image.url}"/>')
        return 'NO IMAGE'

    get_image.short_description = 'image'

    def get_image_detail(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<image width="150px" src="{obj.image.url}"/>')
        return 'NO IMAGE'

    get_image_detail.short_description = 'Show image'


admin.site.site_header = "Social Network"
admin.site.site_title = "Social Network"
