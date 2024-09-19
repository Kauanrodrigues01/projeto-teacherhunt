from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User, Teacher, Student

class TestBaseCreateClassroomView(TestCase):
    def setUp(self):
        self.tomorrow = self.create_tomorrow_date()
        self.yesterday = self.create_yesterday_date()
        self.today = self.create_today_date()

        self.client = APIClient()
        self.url = reverse('students:student-create-classroom')
        self.user_student = User.objects.create_user(
            email='user@example.com',
            password='@Password1234',
            is_student=True,
            is_active=True
        )
        self.student = Student.objects.create(user=self.user_student, name='Student Teste')

        self.user_teacher = User.objects.create_user(
            email='teacher@example.com',
            password='@Password1234',
            is_teacher=True,
            is_active=True
        )  
        self.teacher = Teacher.objects.create(
            user=self.user_teacher, 
            name='Teacher Teste',
            age=30,
            description='Description teacher',
            hourly_price=50.00
        )

        self.data = {
            'professor': self.teacher.id,
            'dia_da_aula': str(self.tomorrow),
            'horario_de_inicio': '12:00',
            'numero_de_horas': 1,
            'descricao_da_aula': 'Aula de teste'
        }

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
    
    def create_today_date(self):
        now = timezone.now()
        return now.date()
    
    def create_tomorrow_date(self):
        now = timezone.now()
        date_now = now.date()
        tomorrow = date_now + timedelta(days=1)
        return tomorrow
    
    def create_yesterday_date(self):
        now = timezone.now()
        date_now = now.date()
        yesterday = date_now - timedelta(days=1)
        return yesterday