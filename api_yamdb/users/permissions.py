from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Доступ к объекту только для админа.
    """

    def has_permission(self, request, view):
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin
