import django.contrib.auth.models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import TeacherSerializer, TeacherProfileImageSerializer, SubjectSerializer
from .permissions import TeacherListPermission, IsTeacherAuthenticated
from rest_framework import viewsets
from accounts.models import Teacher, Subject
from rest_framework.generics import ListAPIView
from rest_framework import status
from classroom.serializers import ClassroomSerializer
from rest_framework.exceptions import NotFound

class TeacherList(APIView):
    permission_classes = (TeacherListPermission,)
    
    def get(self, request):
        q = request.query_params.get("q", "")
        if q != '':
            teachers = Teacher.objects.filter(description__icontains=q)
        else:
            teachers = Teacher.objects.all()
        
        serializer = TeacherSerializer(teachers, many=True, context={'request_method': request.method})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TeacherSerializer(data=request.data, context={'request_method': request.method})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"error": "Professor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeacherSerializer(teacher, data=request.data, partial=True, context={'request_method': request.method})        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"error": "Professor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        teacher.delete()
        teacher.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TeacherProfileImageView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"error": "Professor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherProfileImageSerializer(teacher, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Foto de perfil atualizada com sucesso"})

class TeacherDetail(APIView):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher.objects.all(), pk=pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    
class MeView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"error": "Professor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    
class TeacherListForSubjects(APIView):
    def get(self, request, pk):
        subject = get_object_or_404(Subject.objects.all(), pk=pk)
        teachers = subject.teachers.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    
class SubjectsList(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        name = self.request.query_params.get("name", None)
        queryset = self.queryset
        if name is not None:
            return queryset.filter(name__icontains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAdminUser()]
        return super().get_permissions()
    
class TeacherClassroomView(ListAPIView):
    permission_classes = [IsTeacherAuthenticated]
    serializer_class = ClassroomSerializer
    
    def get_queryset(self):
        user = self.request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            raise NotFound(detail="Aluno não encontrado")

        queryset = teacher.classrooms.all()

        status = self.request.query_params.get('status')
        if status in ['agendado', 'em progresso', 'concluida', 'cancelada']:
            status_mapping = {
                'agendado': 'scheduled',
                'em progresso': 'in_progress',
                'concluida': 'completed',
                'cancelada': 'cancelled'
            }
            queryset = queryset.filter(status=status_mapping[status])
        
        return queryset