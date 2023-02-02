from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsUser(BasePermission):
    allowed_user_roles = 'user'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in SAFE_METHODS:
                return True
        return False


class IsModerator(BasePermission):
    allowed_user_roles = 'moderator'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False


class IsAdmin(BasePermission):
    allowed_user_roles = 'admin'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False
