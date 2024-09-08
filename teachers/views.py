import django.contrib.auth.models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import TeacherSerializer, TeacherProfileImageSerializer, SubjectSerializer
from .permissions import TeacherListPermission
from rest_framework import viewsets
from accounts.models import Teacher, Subject

class TeacherList(APIView):
    permission_classes = (TeacherListPermission,)
    
    def get(self, request):
        q = request.query_params.get("q", "")
        if q != '':
            teachers = Teacher.objects.filter(description__icontains=q)
        else:
            teachers = Teacher.objects.all()    
        
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TeacherProfileImageView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        serializer = TeacherProfileImageSerializer(request.user, data=request.data)
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
        serializer = TeacherSerializer(request.user)
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
        code = self.request.query_params.get("code", None)
        name = self.request.query_params.get("name", None)
        if code is not None:
            print(f"Filtrando por código: {code}")
            return Subject.objects.filter(code=code)
        if name is not None:
            print(f"Filtrando por nome: {name}")
            return Subject.objects.filter(name__icontains=name)
        return Subject.objects.all()

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