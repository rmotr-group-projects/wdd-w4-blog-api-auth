from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # implement your logic here
    #exceptions.PermissionDenied or exceptions.NotAuthenticated
    def has_permission(self, request, view):
        pass 
    
    def has_object_permission(self, request, view, obj):
        pass
