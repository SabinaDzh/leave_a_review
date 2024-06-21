import enum


class UserRoles(enum.Enum):
    """Роли пользователей"""

    admin = 'admin'
    moderator = 'moderator'
    user = 'user'
