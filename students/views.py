from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import StudentSerializer, StudentProfileImageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from accounts.models import Student
from .permissions import StudentListPermission

class StudentList(APIView):
    permission_classes = (StudentListPermission,)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data, context={'request_method': request.method})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data, partial=True, context={'request_method': request.method})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
class StudentProfileImageView(APIView):
    def post(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentProfileImageSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Foto de perfil atualizada com sucesso"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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