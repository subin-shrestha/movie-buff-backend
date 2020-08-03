from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_verified)
