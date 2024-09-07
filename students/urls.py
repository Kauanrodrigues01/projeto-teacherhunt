from django.urls import path
from core.urls import app_name
from .views import StudentList, TeacherStudentList

app_name = 'students'
urlpatterns = [
    path('professores/<int:teacher_pk>/alunos', StudentList.as_view(), name='list'),
    path("professores/alunos", TeacherStudentList.as_view(), name="teacher-students"),
]
