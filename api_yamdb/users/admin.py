from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id',
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'role',
                    'bio',
                    )
    search_fields = ('username', )
    empty_value_display = '-пусто-'
    list_editable = ('role',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('bio', 'role',)}),
    )
