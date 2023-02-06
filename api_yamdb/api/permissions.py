from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUser(BasePermission):
    allowed_user_roles = 'user'

    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.role in self.allowed_user_roles
        ):
            if request.user.method in SAFE_METHODS:
                return True
            return True


class IsModerator(BasePermission):
    allowed_user_roles = 'moderator'

    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.role in self.allowed_user_roles
        ):
            if request.user.method in SAFE_METHODS:
                return True
            return True


class AdminOrSuperUser(BasePermission):
    allowed_user_roles = 'admin'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if (
                request.user.role in self.allowed_user_roles
                or request.user
                and request.user.is_superuser
            ):
                return True
        return False


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )


class IsModeratorOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.role == 'moderator'
            or request.user == obj.author
            or request.method in SAFE_METHODS
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
