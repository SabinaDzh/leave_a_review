from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    """Роли пользователей"""

    admin = 'admin', _('Администратор')
    moderator = 'moderator', _('Модератор')
    user = 'user', _('Пользователь')
