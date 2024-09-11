from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, Teacher, Subject
from teachers.serializers import TeacherSerializer
from .base.test_base_teacher_view import TeacherListBase

class TeacherListTests(TeacherListBase):
    def test_get_teachers(self):
        response = self.client.get(self.url)
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_teacher(self):
        data = {
            "nome": "Jane Doe",
            "descricao": "An excellent teacher",
            "valor_hora": 60.00,
            "idade": 28,
            "materias": [self.subject.id],
            "email": "jane@example.com",
            "password": "@Password1234",
            "password_confirmation": "@Password1234"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Teacher.objects.filter(name="Jane Doe").exists())

    def test_put_teacher(self):
        token = self.obtain_token()
        subject2 = Subject.objects.create(name='Physics')
        data = {
            "nome": "John Smith",
            "descricao": "An updated description",
            "valor_hora": 70.00,
            "idade": 35,
            "materias": [subject2.id],
            "email": "putemail@gmail.com",
            "password": "@Putpassword1234",
            "password_confirmation": "@Putpassword1234"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db() # self.teacher.refresh_from_db() é uma função que atualiza o objeto self.teacher com os dados mais recentes do banco de dados, neste caso, após a requisição PUT.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.teacher.name, data['nome'])
        self.assertEqual(self.teacher.description, data['descricao'])
        self.assertEqual(self.teacher.hourly_price, data['valor_hora'])
        self.assertEqual(self.teacher.age, data['idade'])
        self.assertEqual(self.teacher.subjects.first().name, subject2.name)
        self.assertEqual(self.teacher.user.email, data['email'])
        
    def test_partial_update_put_teacher(self):
        token = self.obtain_token()
        subject2 = Subject.objects.create(name='Physics')
        data = {
            "nome": "John Smith",
            "materias": [self.subject.id, subject2.id]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.name, data['nome'])
        self.assertEqual(self.teacher.subjects.count(), 2)
        self.assertEqual(list(self.teacher.subjects.values_list('id', flat=True)), data["materias"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_delete_teacher(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Teacher.objects.filter(id=self.teacher.id).exists())
    
    # def test_partial_update_just_password_put_teacher(self):
    #     token = self.obtain_token()
    #     data = {
    #         "password": "@NewPassword1234",
    #         "password_confirmation": "@Newpassword1234"
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    #     response = self.client.put(self.url, data, format='json')
    #     self.teacher.refresh_from_db()
    #     self.teacher.user.refresh_from_db()
    #     token = self.obtain_token(password=data['password'])
    #     if token == False:
    #        self.fail('Password not updated')
    #     self.assertTrue(True)
    
    # def test_partial_update_just_email_put_teacher(self):
    #     token = self.obtain_token()
    #     data = {
    #         "email": "testputemail@gamil.com"
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    #     self.client.put(self.url, data, format='json')
    #     self.teacher.refresh_from_db()
    #     self.teacher.user.refresh_from_db()
    #     self.assertEqual(self.teacher.user.email, data['email'])

