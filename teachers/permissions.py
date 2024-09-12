from rest_framework.permissions import BasePermission, SAFE_METHODS

class TeacherListPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user.is_authenticated and request.user.is_teacher
        if request.method == 'POST':
            return not request.user.is_authenticated
        return super().has_permission(request, view)


class IsTeacherAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher