from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import TeacherSerializer, TeacherProfileImageSerializer, SubjectSerializer
from .permissions import TeacherListPermission, IsTeacherAuthenticated
from rest_framework import viewsets
from accounts.models import Rating, Subject, Teacher
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from classroom.serializers import ClassroomSerializer
from rest_framework.exceptions import NotFound
from classroom.models import Classroom
from django.utils import timezone
from django.db.models import Q, Avg
from students.serializers import RatingSerializer

class TeacherList(APIView):
    permission_classes = (TeacherListPermission,)
    
    def get(self, request):
        q = request.query_params.get('q', '')
        query = Q()

        if q:
            search_terms = q.split()
            for term in search_terms:
                term = term.strip()
                if len(term) > 3: 
                    query |= Q(description__icontains=term) | Q(subjects__name__icontains=term)

        # Inicializa teachers com todos os professores, aplicando a busca se necessário
        teachers = Teacher.objects.filter(user__is_active=True)  # Filtra os professores ativos

        if query:
            teachers = teachers.filter(query)

        avaliacao_min = request.query_params.get('avaliacao_min', None)
        try:
            avaliacao_min = float(avaliacao_min) if avaliacao_min else None
        except (ValueError, TypeError):
            avaliacao_min = None 

        if avaliacao_min is not None:
            # Calcular a média das avaliações e filtrar os professores
            teachers = teachers.annotate(media_avaliacao=Avg('ratings__rating')).filter(media_avaliacao__gte=avaliacao_min)
            
        preco_max = request.query_params.get('preco_max', None)
        if preco_max:
            teachers = teachers.filter(hourly_price__lte=preco_max)

        # Ordena e serializa os professores filtrados
        teachers = teachers.order_by('-id')
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
            return Response({'error': 'Professor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TeacherSerializer(teacher, data=request.data, partial=True, context={'request_method': request.method})        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({'error': 'Professor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        if teacher.classrooms.all().filter(status='A', day_of_class__gt=timezone.now().date()).exists():
            return Response({'error': 'Você não pode excluir sua conta enquanto tiver aulas aceitas.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deleta o professor e o usuário associado
        teacher.delete()
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TeacherProfileImageView(APIView):
    permission_classes = (IsTeacherAuthenticated,)
    
    def post(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({'error': 'Professor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherProfileImageSerializer(teacher, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Foto de perfil atualizada com sucesso'})

class TeacherDetail(APIView):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher.objects.all(), pk=pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    
class TeacherMeView(APIView):
    permission_classes = (IsTeacherAuthenticated,)
    
    def get(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({'error': 'Professor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    
class TeacherListForSubjects(APIView):
    def get(self, request, pk):
        subject = get_object_or_404(Subject.objects.all(), pk=pk)
        teachers = subject.teachers.all().order_by('-id')
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SubjectsList(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('id')
    serializer_class = SubjectSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        name = self.request.query_params.get('nome', None)
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
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        elif self.request.method in ['POST', 'PUT', 'DELETE']:
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
            raise NotFound(detail='Aluno não encontrado')

        queryset = teacher.classrooms.all().order_by('day_of_class', 'start_time')

        status = self.request.query_params.get('status')
        if status in ['pendente', 'aceita', 'cancelada']:
            status_mapping = {
                'pendente': 'P',
                'aceita': 'A',
                'cancelada': 'C'
            }
            queryset = queryset.filter(status=status_mapping[status])
        
        return queryset

class TeacherClassroomDetailView(RetrieveAPIView):
    permission_classes = [IsTeacherAuthenticated]
    serializer_class = ClassroomSerializer
    
    def get_queryset(self):
        user = self.request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            raise NotFound(detail='Professor não encontrado')

        queryset = teacher.classrooms.all().order_by('day_of_class', 'start_time')
        return queryset
    
    def get_object(self, **kwargs):
        try:
            classroom = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        except:
            raise NotFound(detail='Aula não encontrada')
        if self.get_queryset().count() == 0:
            raise NotFound(detail='Aula não encontrada')
        self.check_object_permissions(self.request, classroom)
        return classroom

class TeacherAcceptedClassroomView(APIView):
    permission_classes = [IsTeacherAuthenticated]
    
    def post(self, request, pk):
        user = request.user
        classroom = get_object_or_404(Classroom.objects.all(), pk=pk)
        if user != classroom.teacher.user:
            return Response({'error': 'Você não tem permissão para aceitar essa aula.'}, status=status.HTTP_403_FORBIDDEN)
        if classroom.status != 'P':
            return Response({'error': 'A aula já foi aceita ou cancelada, não é possível alterar.'}, status=status.HTTP_400_BAD_REQUEST)
        if classroom.start_time < timezone.now().time() and classroom.day_of_class == timezone.now().date():
            classroom.status = 'C'
            classroom.save()
            return Response({'error': 'Já passou o horário da aula, não é possível aceitar.'}, status=status.HTTP_400_BAD_REQUEST)
    
        classroom.status = 'A'
        classroom.save()
        return Response({'message': 'Aula aceita com sucesso.'}, status=status.HTTP_200_OK)
    
class TeacherCancelledClassroomView(APIView):
    permission_classes = [IsTeacherAuthenticated]
    
    def post(self, request, pk):
        user = request.user
        classroom = get_object_or_404(Classroom.objects.all(), pk=pk)
        if user != classroom.teacher.user:
            return Response({'error': 'Você não tem permissão para cancelar essa aula.'}, status=status.HTTP_403_FORBIDDEN)
        if classroom.status != 'P':
            return Response({'error': 'Aula já foi aceita ou cancelada, não é possivel mudar.'}, status=status.HTTP_400_BAD_REQUEST)
        if classroom.status == 'C':
            return Response({'error': 'Aula já foi cancelada.'}, status=status.HTTP_400_BAD_REQUEST)
        if classroom.start_time < timezone.now().time() and classroom.day_of_class == timezone.now().date():
            classroom.status = 'C'
            classroom.save()
            return Response({'error': 'Já passou o horário da aula, não é possivel cancelar.'}, status=status.HTTP_400_BAD_REQUEST)

        classroom.status = 'C'
        classroom.save()
        return Response({'message': 'Aula recusada com sucesso.'}, status=status.HTTP_200_OK)
    
class TeacherRatingsView(APIView):
    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            return Response({'error': 'Professor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        ratings = teacher.ratings.all()

        if ratings.count() == 0:
            return Response({'error': 'Nenhuma avaliação encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
