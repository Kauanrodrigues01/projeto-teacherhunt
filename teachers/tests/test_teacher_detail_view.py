from rest_framework import status
from django.urls import reverse
from teachers.serializers import TeacherSerializer
from .base.test_base_teacher_view import TeacherTestBase

class TeacherDetailTests(TeacherTestBase):
    def test_get_teacher_detail(self):
        response = self.client.get(reverse('teachers:detail', args=[self.teacher.id]))
        serializer = TeacherSerializer(self.teacher)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)