from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to Admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Admin')

class IsAnalyst(permissions.BasePermission):
    """
    Allows access only to Analyst users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Analyst')

class IsViewer(permissions.BasePermission):
    """
    Allows access only to Viewer users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Viewer')

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object (or admins) to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.role == 'Admin':
            return True
        # Others must be owner
        return obj.user == request.user
