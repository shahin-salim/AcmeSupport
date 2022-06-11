from rest_framework import permissions
from accounts.decorator import is_user_is_authenticated
from accounts.decorator import decode_jwt
from accounts.models import CustomUser


class AdminOnly(permissions.BasePermission):
    """
    fix_an_appointment
    """

    def has_permission(self, request, view):
        decoded = decode_jwt(request)

        try:
            decoded = decode_jwt(request)
            if CustomUser.objects.get(id=decoded["userId"]).role == "admin":
                return True
        except:
            pass
        return False
