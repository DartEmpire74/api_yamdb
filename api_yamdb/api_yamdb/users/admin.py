from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
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


admin.site.register(User)
