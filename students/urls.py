from django.urls import path
from core.urls import app_name
from .views import StudentList

app_name = 'students'
urlpatterns = [
    path('alunos', StudentList.as_view(), name='list'),
    # path("alunos/agendar-aula/<int:teacher_pk>", StudentCreateClassRoom.as_view(), name="create-classroom"),
    # path("professores/alunos", TeacherStudentList.as_view(), name="teacher-students"),
]
