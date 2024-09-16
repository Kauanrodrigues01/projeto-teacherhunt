from rest_framework import status
from accounts.models import Teacher, Subject, User
from teachers.serializers import TeacherSerializer
from .base.test_base_teacher_view import TeacherTestBase
from django.core.files.uploadedfile import SimpleUploadedFile

class TeacherListTests(TeacherTestBase):
    def test_get_teachers(self):
        response = self.client.get(self.url)
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_teacher(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Teacher.objects.filter(name=self.data['nome']).exists())

    def test_post_teacher_with_invalid_email(self):
        self.data['email'] = 'janeexample.com',
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Teacher.objects.filter(name=self.data['nome']).exists())
        self.assertEqual(response.data['email'][0], 'Insira um endereço de email válido.')

    def test_post_teacher_with_invalid_password(self):
        self.data['password'] = 'password'
        self.data['password_confirmation'] = 'password'

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Teacher.objects.filter(name=self.data['nome']).exists())
        self.assertEqual(response.data['password'][0], 'A senha deve conter pelo menos uma letra maiúscula.')
        self.assertEqual(response.data['password'][1], 'A senha deve conter pelo menos um número.')
        self.assertEqual(response.data['password'][2], 'A senha deve conter pelo menos um caractere especial (@, #, $, %, etc.).')

    def test_post_teacher_with_password_confirmation_not_matching(self):
        self.data['password'] = '@Password123'
        self.data['password_confirmation'] = '@Password1234'

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Teacher.objects.filter(name=self.data['nome']).exists())
        self.assertEqual(response.data['password'][0], 'As senhas não conferem.')

    def test_post_teacher_with_email_already_registered(self):
        self.client.post(self.url, self.data, format='json')
        self.data['nome'] = 'Teacher alternative'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'Este email já está cadastrado')
    
    def test_post_teacher_with_empty_name(self):
        self.data['nome'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'Este campo não pode ser em branco.')

    def test_post_teacher_with_name_only_numbers(self):
        self.data['nome'] = '1234'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'O nome deve conter apenas letras.')

    def test_post_teacher_with_name_special_characters(self):
        self.data['nome'] = '@#$%&*'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'O nome deve conter apenas letras.')

    def test_post_teacher_with_name_less_than_3_characters(self):
        self.data['nome'] = 'Jo'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'O nome deve ter no mínimo 3 caracteres.')

    def test_post_teacher_with_name_greater_than_100_characters(self):
        self.data['nome'] = 'J' * 256
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'O nome deve ter no máximo 100 caracteres.')

    def test_post_teacher_with_empty_description(self):
        self.data['descricao'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['descricao'][0], 'Este campo não pode ser em branco.')

    def test_post_teacher_with_description_only_numbers(self):
        self.data['descricao'] = '1234567890'
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['descricao'][0], 'A descrição não pode ser apenas números.')

    def test_post_teacher_with_age_empty(self):
        self.data['idade'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['idade'][0], 'Um número inteiro válido é exigido.')

    def test_post_teacher_with_age_less_than_10(self):
        self.data['idade'] = -1
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['idade'][0], 'A idade deve ser maior ou igual a 18.')

    def test_post_teacher_with_age_greater_than_100(self):
        self.data['idade'] = 101
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['idade'][0], 'A idade deve ser menor ou igual a 100.')

    def test_post_teacher_with_hourly_price_empty(self):
        self.data['valor_hora'] = ''
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valor_hora'][0], 'Um número válido é necessário.')

    def test_post_teacher_with_hourly_price_less_than_10(self):
        self.data['valor_hora'] = -1
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valor_hora'][0], 'O valor por hora deve ser maior que 10.')

    def test_post_teacher_without_the_name(self):
        del self.data['nome']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['nome'][0], 'Este campo é obrigatório.')

    def test_post_teacher_without_the_description(self):
        del self.data['descricao']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['descricao'][0], 'Este campo é obrigatório.')
    
    def test_post_teacher_without_the_hourly_price(self):
        del self.data['valor_hora']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['valor_hora'][0], 'Este campo é obrigatório.')

    def test_post_teacher_without_the_age(self):
        del self.data['idade']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['idade'][0], 'Este campo é obrigatório.')

    def test_post_teacher_without_the_subjects(self):
        del self.data['materias']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['materias'][0], 'Este campo é obrigatório.')

    def test_put_all_fields_teacher(self):
        token = self.obtain_token()
        subject2 = Subject.objects.create(name='Physics')
        data = {
            'nome': 'John Smith',
            'descricao': 'An updated description',
            'valor_hora': 70.00,
            'idade': 35,
            'materias': [subject2.id],
            'email': 'putemail@gmail.com',
            'password': '@Putpassword1234',
            'password_confirmation': '@Putpassword1234'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.teacher.name, data['nome'])
        self.assertEqual(self.teacher.description, data['descricao'])
        self.assertEqual(self.teacher.hourly_price, data['valor_hora'])
        self.assertEqual(self.teacher.age, data['idade'])
        self.assertEqual(self.teacher.subjects.first().name, subject2.name)
        self.assertEqual(self.teacher.user.email, data['email'])
    
    def test_partial_update_name_put_teacher(self):
        token = self.obtain_token()
        data = {
            'nome': 'John Smith'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.name, data['nome'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_partial_update_description_put_teacher(self):
        token = self.obtain_token()
        data = {
            'descricao': 'An updated description'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.description, data['descricao'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_hourly_price_put_teacher(self):
        token = self.obtain_token()
        data = {
            'valor_hora': 70.00,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.hourly_price, data['valor_hora'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_age_put_teacher(self):
        token = self.obtain_token()
        data = {
            'idade': 25,
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.age, data['idade'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_subjects_put_teacher(self):
        token = self.obtain_token()
        subject2 = Subject.objects.create(name='Physics')
        data = {
            'materias' : [self.subject.id, subject2.id],
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertIn(subject2, self.teacher.subjects.all())
        self.assertIn(self.subject, self.teacher.subjects.all())
        self.assertEqual(data['materias'], list(self.teacher.subjects.values_list('id', flat=True)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_email_put_teacher(self):
        token = self.obtain_token()
        data = {
            'email' : 'putemail@gmail.com',
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.user.email, data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_password_put_teacher(self):
        token = self.obtain_token()
        data = {
            'password': '@Putpassword1234',
            'password_confirmation': '@Putpassword1234'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        
        token = self.obtain_token(password=data['password'])
        self.assertTrue(self.teacher.user.check_password(data['password']))
        self.assertNotEqual(token, False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_partial_profile_image_put_teacher(self):
        token = self.obtain_token()
        self.teacher.profile_image = self.image
        self.teacher.save()
        self.assertIn('media/teachers_image/test_image', self.teacher.profile_image.url)
        self.assertIn('jpg', self.teacher.profile_image.url)
        
        data = {
            'foto': SimpleUploadedFile('test_image_update.png', self.create_test_image().read()),
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='multipart')
        self.teacher.refresh_from_db()
        
        self.assertIsNotNone(self.teacher.profile_image.url)
        self.assertIn('media/teachers_image/test_image_update', self.teacher.profile_image.url)
        self.assertIn('png', self.teacher.profile_image.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_teacher(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Teacher.objects.filter(id=self.teacher.id).exists())

    def test_whether_when_deleting_the_teacher_it_deletes_the_user_related_to_the_teacher(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.teacher.user.id).exists())