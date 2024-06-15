from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права для работы с категориями и жанрами."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminRole(permissions.BasePermission):
    """
    Доступ к объектам только для админа.
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    Доступ всем пользователям на чтение.
    Доступ на создание отзыва для аутентифицированных пользователей.
    Доступ на редактирование только авторам, админам, модераторам.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.is_admin or request.user.is_moderator)
