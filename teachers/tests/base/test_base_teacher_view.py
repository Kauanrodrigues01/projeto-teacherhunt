from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, Teacher, Subject
from rest_framework.exceptions import ErrorDetail

class TeacherListBase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('teachers:list')

        # Criar um usuário
        self.user = User.objects.create_user(email='teacher@example.com', password='@Password1234', is_teacher=True)
        self.teacher = Teacher.objects.create(
            user=self.user,
            name='John Doe',
            description='A nice teacher',
            hourly_price=50.00,
            age=30
        )
        self.subject = Subject.objects.create(name='Math')
        
    def obtain_token(self, email='teacher@example.com', password='@Password1234'):
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
            'email': 'teacher@example.com',
            'password': '@Password1234'
        })
        return response_token.data['refresh_token']
    
    