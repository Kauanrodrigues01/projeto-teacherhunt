from django.test import TestCase
from accounts.models import User, Teacher, Student
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

class TestBaseAuthentication(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_student = User.objects.create_user(
            email='studentteste@gmail.com',
            password='@Student123',
            is_student=True,
            is_active=True
        )
        self.student = Student.objects.create(
            user=self.user_student,
            name='Student Teste'
        )

        self.user_teacher = User.objects.create_user(
            email='teacherteste@gmail.com',
            password='@Teacher123',
            is_teacher=True,
            is_active=True
        )
        self.teacher = Teacher.objects.create(
            user=self.user_teacher,
            name='Teacher Teste',
            hourly_price=50.00,
            age=30,
            description='Teacher Teste Description'
        )

    def obtain_token_teacher(self, email='teacherteste@gmail.com', password='@Teacher123'):
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
    
    def obtain_token_student(self, email='studentteste@gmail.com', password='@Student123'):
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