from rest_framework import status
from accounts.models import Student
from .base.test_base_student_view import StudentTestBase
from django.core.files.uploadedfile import SimpleUploadedFile

class studentListTests(StudentTestBase):
    def test_post_student(self):
        data = {
            "nome": "Jane Doe",
            "email": "jane@example.com",
            "password": "@Password1234",
            "password_confirmation": "@Password1234"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(name=data["nome"]).exists())

    def test_put_all_fields_student(self):
        token = self.obtain_token()
        data = {
            "nome": "John Smith",
            "email": "putemail@gmail.com",
            "password": "@Putpassword1234",
            "password_confirmation": "@Putpassword1234"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.student.refresh_from_db()
        self.student.user.refresh_from_db()
        self.assertEqual(self.student.name, data['nome'])
        self.assertEqual(self.student.user.email, data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_name_put_student(self):
        token = self.obtain_token()
        data = {
            'nome': 'John Smith'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, data['nome'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_email_put_student(self):
        token = self.obtain_token()
        data = {
            'email' : 'putemail@gmail.com',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.student.refresh_from_db()
        self.assertEqual(self.student.user.email, data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_password_put_student(self):
        token = self.obtain_token()
        data = {
            'password': '@Putpassword1234',
            'password_confirmation': '@Putpassword1234'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.student.refresh_from_db()
        
        token = self.obtain_token(password=data['password'])
        self.assertTrue(self.student.user.check_password(data['password']))
        self.assertNotEqual(token, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_partial_profile_image_put_student(self):
        token = self.obtain_token()
        self.student.profile_image = self.image
        self.student.save()
        self.assertIn('media/students_image/test_image', self.student.profile_image.url)
        self.assertIn('jpg', self.student.profile_image.url)
        
        data = {
            'foto': SimpleUploadedFile('test_image_update.png', self.create_test_image().read()),
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='multipart')
        self.student.refresh_from_db()
        
        self.assertIsNotNone(self.student.profile_image.url)
        self.assertIn('media/students_image/test_image_update', self.student.profile_image.url)
        self.assertIn('png', self.student.profile_image.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_delete_student(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())