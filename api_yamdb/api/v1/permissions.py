from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUser(BasePermission):
    allowed_user_roles = 'user'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in self.allowed_user_roles
                or request.user.method in SAFE_METHODS)


class IsModerator(BasePermission):
    allowed_user_roles = 'moderator'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in self.allowed_user_roles
                or request.user.method in SAFE_METHODS)


class AdminOrSuperUser(BasePermission):
    allowed_user_roles = 'admin'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role in self.allowed_user_roles
                or request.user
                and request.user.is_superuser)


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class ReviewPermission(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)
