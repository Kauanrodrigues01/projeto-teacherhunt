from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStudentAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student