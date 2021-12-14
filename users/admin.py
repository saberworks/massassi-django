from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'date_joined', 'created_at')
    list_filter = ('is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
