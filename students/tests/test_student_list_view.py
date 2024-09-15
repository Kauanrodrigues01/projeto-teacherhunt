from rest_framework import status
from accounts.models import Student, User
from .base.test_base_student_view import StudentTestBase
from django.core.files.uploadedfile import SimpleUploadedFile

class studentListTests(StudentTestBase):
    def test_post_student(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(name=self.data['nome']).exists())
        self.assertTrue(User.objects.filter(email=self.data['email']).exists())

    def test_post_student_with_invalid_email(self):
        self.data['email'] = 'janeexample.com',
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Student.objects.filter(name=self.data['nome']).exists())

    def test_post_student_with_invalid_password(self):
        self.data['password'] = 'password'
        self.data['password_confirmation'] = 'password'

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Student.objects.filter(name=self.data['nome']).exists())
        self.assertEqual(response.data['password'][0], 'A senha deve conter pelo menos uma letra maiúscula.')
        self.assertEqual(response.data['password'][1], 'A senha deve conter pelo menos um número.')
        self.assertEqual(response.data['password'][2], 'A senha deve conter pelo menos um caractere especial (@, #, $, %, etc.).')

    def test_post_student_with_password_confirmation_not_matching(self):
        self.data['password'] = '@Password123'
        self.data['password_confirmation'] = '@Password1234'

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Student.objects.filter(name=self.data['nome']).exists())
        self.assertEqual(response.data['password'][0], 'As senhas não conferem.')

    def test_post_student_with_email_already_registered(self):
        self.client.post(self.url, self.data, format='json')
        self.data['nome'] = 'Student alternative'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)
        self.assertEqual(response.data['email'][0], 'Este email já está cadastrado')

    def test_post_student_with_empty_name(self):
        self.data['nome'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'Este campo não pode ser em branco.')

    def test_post_student_with_name_only_numbers(self):
        self.data['nome'] = '1234'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'O nome não pode ser apenas números.')

    def test_post_student_with_name_less_than_5_characters(self):
        self.data['nome'] = 'Jo'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'O nome deve ter no mínimo 5 caracteres.')

    def test_post_student_with_name_greater_than_255_characters(self):
        self.data['nome'] = 'a'*266
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'O nome deve ter no máximo 255 caracteres.')

    def test_post_student_with_empty_email(self):
        self.data['email'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'Este campo não pode ser em branco.')

    def test_post_student_with_empty_password(self):
        self.data['password'] = ''
        self.data['password_confirmation'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], 'Este campo não pode ser em branco.')
        self.assertEqual(response.data['password_confirmation'][0], 'Este campo não pode ser em branco.')

    def test_put_all_fields_student(self):
        token = self.obtain_token()
        data = {
            'nome': 'John Smith',
            'email': 'putemail@gmail.com',
            'password': '@Putpassword1234',
            'password_confirmation': '@Putpassword1234'
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