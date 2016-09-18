from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # implement your logic here
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # print(obj.users)
        # print((obj))
        # print((obj.users.all()))
        # print(request.user in obj.users.all())
        # print(request.user in obj.users)
        return request.user in obj.users.all()
