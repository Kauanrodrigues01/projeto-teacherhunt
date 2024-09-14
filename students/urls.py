from django.urls import path
from .views import StudentList, StudentProfileImageView, StudentClassroomView, StudentClassroomDetailView

app_name = 'students'
urlpatterns = [
    path('alunos', StudentList.as_view(), name='list'),
    path('alunos/foto', StudentProfileImageView.as_view(), name='profile-image'),
    path('alunos/aulas', StudentClassroomView.as_view(), name='student-classrooms'),
    path('alunos/aulas/<int:pk>', StudentClassroomDetailView.as_view(), name='student-classroom-detail')
]
