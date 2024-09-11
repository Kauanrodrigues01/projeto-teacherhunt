from rest_framework import status
from django.urls import reverse
from accounts.models import User, Teacher, Subject
from teachers.serializers import TeacherSerializer
from .base.test_base_teacher_view import TeacherListBase

class MeViewTest(TeacherListBase):
    def test_logged_teacher(self):
        token = self.obtain_token()
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.url, format='json')
        teacher_serializer = TeacherSerializer(self.teacher)
        self.assertEqual(response.data[0], teacher_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)