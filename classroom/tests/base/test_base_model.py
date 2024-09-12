from django.test import TestCase
from accounts.models import Student, Teacher, User
from classroom.models import Classroom
from datetime import datetime, timedelta
from django.utils import timezone

class TestBaseModelClassroom(TestCase):
    def setUp(self) -> None:
        self.tomorrow = self.create_tomorrow_date()
        self.yesterday = self.create_yesterday_date()
        self.today = self.create_today_date()
        return super().setUp()
    
    def create_classroom(self, student, teacher, day_of_class, start_time, number_of_hours):
        classroom = Classroom.objects.create(
            student=student,
            teacher=teacher,
            day_of_class=day_of_class,
            start_time=start_time,
            number_of_hours=number_of_hours,
            description_about_class='Aula de demonstração'
        )
        
        return classroom
    
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
    
    def create_users_patterns(self):
        student = self.create_student()
        teacher = self.create_teacher()
        return {'student': student, 'teacher': teacher}
    
    def create_student(self):
        user_student = User.objects.create_user(
            email='testemailstudent@gmail.com',
            password='testpasswordstudent',
            is_student=True
        )
        student = Student.objects.create(
            user=user_student,
            name='John Cena'
        )
        return student
    
    def create_teacher(self):
        user_teacher = User.objects.create_user(
            email='testemailteacher@gmail.com',
            password='testpasswordteacher',
            is_teacher=True
        )
        teacher = Teacher.objects.create(
            user=user_teacher,
            name='Ric Flair',
            age=50,
            description='The Nature Boy',
            hourly_price=100
        )
        return teacher