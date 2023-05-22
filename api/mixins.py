from rest_framework import permissions


class AuthPermissionMixin:
    """
    The general permission required to perform most actions, outside the AdminUser
    """
    permission_classes = [permissions.IsAuthenticated]


class AdminPermissionMixin:
    """
    The permission for only AdminUser
    """
    permission_classes = [permissions.IsAdminUser]
