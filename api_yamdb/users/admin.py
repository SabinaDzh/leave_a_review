from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UserAdminParentClass


User = get_user_model()


class UserAdmin(UserAdminParentClass):
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
