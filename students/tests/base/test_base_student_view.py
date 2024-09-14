from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, Student
from rest_framework.exceptions import ErrorDetail
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

class StudentTestBase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('students:list')

        # Criar um usuário
        self.user = User.objects.create_user(email='user@example.com', password='@Password1234', is_student=True)
        self.student = Student.objects.create(
            user=self.user,
            name='John Doe',
        )
        self.image = SimpleUploadedFile('test_image.jpg', self.create_test_image().read())
        
    def obtain_token(self, email='user@example.com', password='@Password1234'):
        login_url = reverse('accounts:login')
        response_token = self.client.post(login_url, {
            'email': email,
            'password': password
        })
        if 'token' not in response_token.data:
            if 'detail' in response_token.data:
                if 'detail' in response_token.data and isinstance(response_token.data['detail'], ErrorDetail):
                    return False
            return False
        return response_token.data['token']
    
    def obtain_refresh_token(self):
        login_url = reverse('accounts:login')
        response_token = self.client.post(login_url, {
            'email': 'user@example.com',
            'password': '@Password1234'
        })
        return response_token.data['refresh_token']
    
    def create_test_image(self):
        image = Image.new('RGB', (100, 100))
        img_io = BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        return img_io
    