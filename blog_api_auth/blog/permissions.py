from rest_framework import permissions

from .models import Entry


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user in obj.users.all()
