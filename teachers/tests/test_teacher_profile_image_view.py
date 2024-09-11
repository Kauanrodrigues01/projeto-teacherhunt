from django.urls import reverse
from rest_framework import status
from .base.test_base_teacher_view import TeacherTestBase

class TeacherProfileImageViewTest(TeacherTestBase):
    def test_upload_image_teacher_related_to_user(self):
        token = self.obtain_token()
        data = {
            'foto': self.image
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(reverse('teachers:profile-image'), data, format='multipart')
        self.teacher.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(self.teacher.profile_image.url)
        self.assertIn('media/teachers_image/test_image', self.teacher.profile_image.url)
        self.assertIn('jpg', self.teacher.profile_image.url)