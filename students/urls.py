from django.urls import path
from .views import StudentList, StudentProfileImageView

app_name = 'students'
urlpatterns = [
    path('alunos', StudentList.as_view(), name='list'),
    path('alunos/foto', StudentProfileImageView.as_view(), name='profile-image')
    # path("alunos/agendar-aula/<int:teacher_pk>", StudentCreateClassRoom.as_view(), name="create-classroom"),
    # path("professores/alunos", TeacherStudentList.as_view(), name="teacher-students"),
]
