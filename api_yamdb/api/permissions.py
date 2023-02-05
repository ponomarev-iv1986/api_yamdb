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


class IsAdmin(BasePermission):
    allowed_user_roles = 'admin'

    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.role in self.allowed_user_roles
        ):
            return True
        return False


class IsSuperUser(BasePermission):
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
