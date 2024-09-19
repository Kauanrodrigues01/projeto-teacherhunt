from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, Teacher, Subject, Student
from rest_framework.exceptions import ErrorDetail
from classroom.models import Classroom
from django.utils import timezone
from datetime import timedelta

class TeacherClassroomTestBase(TestCase):
    def setUp(self):
        self.tomorrow = self.create_tomorrow_date()
        self.yesterday = self.create_yesterday_date()
        self.today = self.create_today_date()
        self.client = APIClient()
        self.user_student = User.objects.create_user(email='user@example.com', password='@Password1234', is_student=True, is_active=True)
        self.student = Student.objects.create(
            user=self.user_student,
            name='John Doe',
        )

        self.user_teacher = User.objects.create_user(email='teacher@example.com', password='@Password1234', is_teacher=True, is_active=True)
        self.teacher = Teacher.objects.create(
            user=self.user_teacher,
            name='John Doe',
            description='A nice teacher',
            hourly_price=50.00,
            age=30
        )

        self.classroom = Classroom.objects.create(
            student=self.student,
            teacher=self.teacher,
            day_of_class=self.tomorrow,
            start_time='12:00',
            end_time='13:00',
            number_of_hours=1
        )

        self.classroom_accepted = Classroom.objects.create(
            student=self.student,
            teacher=self.teacher,
            day_of_class=self.tomorrow,
            start_time='16:00',
            end_time='17:00',
            number_of_hours=1,
            status='A'
        )

        self.classroom_cancelled = Classroom.objects.create(
            student=self.student,
            teacher=self.teacher,
            day_of_class=self.tomorrow,
            start_time='18:00',
            end_time='19:00',
            number_of_hours=1,
            status='C'
        )

        self.teacher_alternative = self.create_teacher(
            email='teacher2alternative@gmail.com', 
            password='@Passwordteacher222',
            name='Teacher 2 teste',
            description='A nice teacher',
            hourly_price=50.00,
            age=30
        )

        self.classroom_alternative = Classroom.objects.create(
            student=self.student,
            teacher=self.teacher_alternative,
            day_of_class=self.tomorrow,
            start_time='14:00',
            end_time='15:00',
            number_of_hours=1
        )

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
    
    def create_teacher(self, email, password, name, description, hourly_price, age):
        user = User.objects.create_user(email=email, password=password, is_teacher=True, is_active=True)
        teacher = Teacher.objects.create(
            user=user,
            name=name,
            description=description,
            hourly_price=hourly_price,
            age=age
        )
        return teacher
    
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