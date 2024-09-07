from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TeacherDetail, TeacherList, MeView, TeacherProfileImageView, TeacherListForSubjects, SubjectsList

app_name = "teachers"

router = SimpleRouter(trailing_slash=False)
router.register(r'subjects', SubjectsList, basename='subjects')

urlpatterns = [
    path("teachers", TeacherList.as_view(), name="list"),
    path("teachers/<int:pk>", TeacherDetail.as_view(), name="detail"),
    path('me', MeView.as_view(), name='me'),
    path("teachers/profile-image", TeacherProfileImageView.as_view(), name="profile-image"),
    path("teachers/<int:pk>/subjects", TeacherListForSubjects.as_view(), name="list-for-teachers"),
    path('', include(router.urls))
]
