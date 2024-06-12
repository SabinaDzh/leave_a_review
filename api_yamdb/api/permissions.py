from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права для работы с категориями и жанрами."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
