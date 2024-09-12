from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import StudentSerializer, StudentProfileImageSerializer
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
            student = Student.objects.select_related('user').get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data, partial=True, context={'request_method': request.method})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        try:
            student = Student.objects.select_related('user').get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
class StudentProfileImageView(APIView):
    def post(self, request):
        user = request.user
        try:
            student = Student.objects.select_related('user').get(user=user)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentProfileImageSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Foto de perfil atualizada com sucesso"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)