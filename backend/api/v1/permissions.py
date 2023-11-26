from rest_framework import permissions


class IsMunicipal(permissions.BasePermission):
    """Предоставляет доступ только муниципальной службе."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_municipal
