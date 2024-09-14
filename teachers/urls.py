from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TeacherDetail, TeacherList, TeacherMeView, TeacherProfileImageView, TeacherListForSubjects, SubjectsList, TeacherClassroomView, TeacherAcceptedClassroomView, TeacherCancelledClassroomView, TeacherClassroomDetailView

app_name = 'teachers'

router = SimpleRouter(trailing_slash=False)
router.register(r'materias', SubjectsList, basename='subjects')

urlpatterns = [
    path('professores', TeacherList.as_view(), name='list'),
    path('professores/<int:pk>', TeacherDetail.as_view(), name='detail'),
    path('professores/me', TeacherMeView.as_view(), name='me'),
    path('professores/foto', TeacherProfileImageView.as_view(), name='profile-image'),
    path('professores/<int:pk>/materias', TeacherListForSubjects.as_view(), name='list-for-subject'),
    path('professores/aulas', TeacherClassroomView.as_view(), name='teacher-classrooms'),
    path('professores/aulas/<int:pk>', TeacherClassroomDetailView.as_view(), name='teacher-classroom-detail'),
    path('professores/aulas/aceitar/<int:pk>', TeacherAcceptedClassroomView.as_view(), name='teacher-accepted-classroom'),
    path('professores/aulas/cancelar/<int:pk>', TeacherCancelledClassroomView.as_view(), name='teacher-cancelled-classroom'),
    path('', include(router.urls))
]
