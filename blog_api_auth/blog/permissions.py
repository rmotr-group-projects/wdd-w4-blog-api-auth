from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # implement your logic here
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user in obj.users.all()
