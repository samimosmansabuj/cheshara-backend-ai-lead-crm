from rest_framework.permissions import BasePermission
from accounts.choices import UserType


class IsClientUser(BasePermission):
    message = "Only authenticated client users are allowed to access this resource."

    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and user.user_type == UserType.CLIENT
        )


class AdminWritePermission(BasePermission):
    message = "Only admin users are allowed to perform write operations."
    def has_permission(self, request, view):
        user = request.user
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return (
                user
                and user.is_authenticated
                and user.user_type == UserType.ADMIN
            )
        return True
