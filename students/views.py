from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class StudentList(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class StudentCreateClassRoom(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, teacher_pk):
#         if not isinstance(request.user, Student):
#             raise PermissionDenied("Você precisa ser um aluno para agendar uma aula.")
        
#         request.data['teacher'] = teacher_pk
#         request.data['student'] = request.user.id
        
#         teacher = get_object_or_404(Teacher, pk=teacher_pk)
        
#         serializer = ClassroomSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(teacher=teacher, student=request.user.student)
        
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class TeacherStudentList(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         if not isinstance(request.user, Teacher):
#             raise PermissionDenied("Você precisa ser um professor para acessar esta lista.")
        
#         students = request.user.classrooms.all()
#         serializer = ClassroomSerializer(students, many=True)
#         return Response(serializer.data)