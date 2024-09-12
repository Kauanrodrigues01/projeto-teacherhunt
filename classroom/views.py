import re
from rest_framework import generics
from .serializers import ClassroomSerializer
from students.permissions import IsStudentAuthenticated
from accounts.models import Student
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ClassroomCreateView(generics.CreateAPIView):
    permission_classes = [IsStudentAuthenticated]
    serializer_class = ClassroomSerializer
    
    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'detail': 'Você não é um estudante.'}, status=status.HTTP_403_FORBIDDEN)
        request.data['student'] = student.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)