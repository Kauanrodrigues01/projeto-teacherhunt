from io import BytesIO
from PIL import Image
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from .base.test_base_student_view import StudentTestBase

class StudentProfileImageViewTest(StudentTestBase):
    def create_test_image(self):
        # Criando uma imagem em branco (RGB) de 100x100 pixels
        image = Image.new('RGB', (100, 100))
        img_io = BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        return img_io

    def test_upload_image_student_related_to_user(self):
        token = self.obtain_token()
        data = {
            'foto': SimpleUploadedFile('test_image.jpg', self.create_test_image().read())
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(reverse('students:profile-image'), data, format='multipart')
        self.student.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(self.student.profile_image.url)
        self.assertIn('media/students_image/test_image', self.student.profile_image.url)
        self.assertIn('jpg', self.student.profile_image.url)