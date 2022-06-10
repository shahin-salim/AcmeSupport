from rest_framework import permissions
from accounts.decorator import is_user_is_authenticated


class FixPermission(permissions.BasePermission):
    """
    fix_an_appointment
    """
    def has_permission(*args):
        print(args)

        return False
