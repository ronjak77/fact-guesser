from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the proposition or answer.
        return obj.owner == request.user

class IsSameUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the user to edit only their own info.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the user themselves.
        return obj == request.user
        
class AllowAddAndRead(permissions.BasePermission):
    """
    Allow creating new objects and read access.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.method == "POST"
        )