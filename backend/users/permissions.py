"""
Role-based permission classes for DRF.

Usage in views:
    permission_classes = [IsAuthenticated, IsDriver]
"""

from rest_framework.permissions import BasePermission


class IsPassenger(BasePermission):
    message = "Only passengers can access this resource."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "passenger"
        )


class IsDriver(BasePermission):
    message = "Only drivers can access this resource."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "driver"
        )


class IsAuthority(BasePermission):
    message = "Only authority users can access this resource."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.role == "authority" or request.user.is_superuser)
        )


class IsOwnerOrAuthority(BasePermission):
    """
    Object-level permission:
    - Authority can do anything.
    - Non-authority users can only touch their own objects.
    """

    message = "You can only access your own resources."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.role == "authority" or user.is_superuser:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "driver", None)
        return owner == user