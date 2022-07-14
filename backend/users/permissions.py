from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    message = 'You already authenticated'

    def has_permission(self, request, view):
        return request.user.is_anonymous
