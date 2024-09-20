from django.urls import path
from .views import StudentList, StudentProfileImageView, StudentClassroomView, StudentClassroomDetailView, StudentMeView, ClassroomCreateView, ClassroomUpdateView, RatingTeacherView

app_name = 'students'
urlpatterns = [
    path('alunos', StudentList.as_view(), name='list'),
    path('alunos/me', StudentMeView.as_view(), name='me'),
    path('alunos/foto', StudentProfileImageView.as_view(), name='profile-image'),
    path('alunos/aulas', StudentClassroomView.as_view(), name='student-classrooms'),
    path('alunos/aulas/<int:pk>', StudentClassroomDetailView.as_view(), name='student-classroom-detail'),
    path('alunos/agendar-aulas', ClassroomCreateView.as_view(), name='student-create-classroom'),
    path('alunos/atualizar-aula/<int:pk>', ClassroomUpdateView.as_view(), name='student-update-classroom'),
    path('alunos/avaliar-professor', RatingTeacherView.as_view(), name='rating-teacher'),
]