from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUserSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
