from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TeacherDetail, TeacherList, TeacherMeView, TeacherProfileImageView, TeacherListForSubjects, SubjectsList, TeacherClassroomView

app_name = "teachers"

router = SimpleRouter(trailing_slash=False)
router.register(r'materias', SubjectsList, basename='subjects')

urlpatterns = [
    path("professores", TeacherList.as_view(), name="list"),
    path("professores/<int:pk>", TeacherDetail.as_view(), name="detail"),
    path('professores/me', TeacherMeView.as_view(), name='me'),
    path("professores/foto", TeacherProfileImageView.as_view(), name="profile-image"),
    path("professores/<int:pk>/materias", TeacherListForSubjects.as_view(), name="list-for-subject"),
    path("professores/aulas", TeacherClassroomView.as_view(), name='teacher-classrooms'),
    path("", include(router.urls))
]
