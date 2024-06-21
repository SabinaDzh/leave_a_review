from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_NAME,
    ROLE_ADMIN_NAME,
    ROLE_MODERATOR_NAME,
    ROLE_USER_NAME)
from users.enums import UserRoles
from users.validators import username_validator


ROLES = [
    (UserRoles.user.value, ROLE_USER_NAME),
    (UserRoles.moderator.value, ROLE_MODERATOR_NAME),
    (UserRoles.admin.value, ROLE_ADMIN_NAME)
]


class User(AbstractUser):

    username = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Ник пользователя',
        unique=True,
        validators=[username_validator,],
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=MAX_LENGTH_NAME,
        blank=True,
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Фамилия пользователя',
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=ROLES,
        default=UserRoles.user.value,
        max_length=max([len(role_name) for role_name, _ in ROLES]),
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.role == UserRoles.admin.value
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == UserRoles.moderator.value
