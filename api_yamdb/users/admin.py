from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    search_fields = ('username',)


admin.site.register(User, UserAdmin)
