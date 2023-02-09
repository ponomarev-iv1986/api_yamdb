from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.userroles import UserRoles


class IsAdminOrSuperuserForUsers(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.role == UserRoles.ADMIN
            or request.user.is_superuser
        )


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.role == UserRoles.ADMIN
            or request.user.is_superuser
        )


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == UserRoles.ADMIN
            or request.user.role == UserRoles.MODERATOR
            or obj.author == request.user
        )
