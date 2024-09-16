import re
from rest_framework import generics
from .serializers import ClassroomSerializer
from students.permissions import IsStudentAuthenticated
from accounts.models import Student
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Classroom
from django.shortcuts import get_object_or_404

class ClassroomView(APIView):
    permission_classes = [IsStudentAuthenticated]
    
    def post(self, request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            return Response({'detail': 'Você não é um estudante.'}, status=status.HTTP_403_FORBIDDEN)
        request.data['aluno'] = student.id
        request.data['status'] = 'P'
        serializer =  ClassroomSerializer(data=request.data, context={'request_method': request.method})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        classroom = get_object_or_404(Classroom.objects.all(), pk=pk)
        if request.user != classroom.student.user:
            return Response({'error': 'Você não tem permissão para alterar esta aula.'}, status=status.HTTP_403_FORBIDDEN)
        if request.data.get('aluno', None) is not None:
            return Response({'error': 'Não é possível alterar o estudante de uma aula.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('professor', None) is not None:
            return Response({'error': 'Não é possível alterar o professor de uma aula.'}, status=status.HTTP_400_BAD_REQUEST)
        if classroom.status != 'P':
            return Response({'error': 'Está aula já foi aceita ou cancelada não é possivel altera-lá.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['aluno'] = classroom.student.id
        data['professor'] = classroom.teacher.id
        serializer =  ClassroomSerializer(instance=classroom, data=data, context={'request_method': request.method})
        serializer.is_valid(raise_exception=True)
        serializer.status = 'P'
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
