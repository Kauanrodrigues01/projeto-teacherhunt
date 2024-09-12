from rest_framework.permissions import BasePermission, SAFE_METHODS

class StudentListPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ["PUT", "DELETE"]:
            return request.user.is_authenticated and request.user.is_student
        if request.method == 'POST':
            return not request.user.is_authenticated
        return super().has_permission(request, view)
    
class IsStudentAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student