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
    Uses 'obj.user' as the ownership link (for Transactions).
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True
        return obj.user == request.user

class IsUserOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission for the User model specifically.
    The owner is the object itself (obj == request.user).
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True
        return obj == request.user
