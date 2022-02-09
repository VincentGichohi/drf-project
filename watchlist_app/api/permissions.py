import re
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
            # Check permissions for read-only request
        else:
            # Check permissions for write request
            return bool(request.user and request.user.is_staff)

class IsReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check permissions for read-only request
        else:
        # Check permissions for write request
            return obj.review_user == request.user or request.user.is_staff