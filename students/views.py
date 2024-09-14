from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StudentSerializer, StudentProfileImageSerializer
from accounts.models import Student
from .permissions import IsStudentAuthenticated, StudentListPermission
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from classroom.serializers import ClassroomSerializer
from rest_framework.exceptions import NotFound

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
    
class StudentClassroomView(ListAPIView):
    permission_classes = [IsStudentAuthenticated]
    serializer_class = ClassroomSerializer
    
    def get_queryset(self):
        user = self.request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise NotFound(detail="Aluno não encontrado")

        queryset = student.classrooms.all().order_by('day_of_class', 'start_time')

        status = self.request.query_params.get('status')
        if status in ['pendente', 'aceita', 'cancelada']:
            status_mapping = {
                'pendente': 'P',
                'aceita': 'A',
                'cancelada': 'C'
            }
            queryset = queryset.filter(status=status_mapping[status])
        
        return queryset

class StudentClassroomDetailView(RetrieveAPIView):
    permission_classes = [IsStudentAuthenticated]
    serializer_class = ClassroomSerializer
    
    def get_queryset(self):
        user = self.request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise NotFound(detail="Professor não encontrado")

        queryset = student.classrooms.all().order_by('day_of_class', 'start_time')
        return queryset
    
    def get_object(self):
        try:
            classroom = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        except:
            raise NotFound(detail="Aula não encontrada")
        if self.get_queryset().count() == 0:
            raise NotFound(detail="Aula não encontrada")
        self.check_object_permissions(self.request, classroom)
        return classroom