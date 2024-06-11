from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
]


class User(AbstractUser):

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    username = models.CharField(
        max_length=150,
        verbose_name='Ник пользователя',
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
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
        default=USER,
        max_length=20,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
