from .base.test_base_model import TestBaseModelClassroom
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils import timezone


class TestClassroomModel(TestBaseModelClassroom):
    def test_returns_an_error_if_an_attempt_is_made_to_create_a_class_overlapping_the_period_of_another_class(self):
        '''Testa se retorna um erro se tentar criar uma aula que se sobrepõe ao período de outra aula'''
        data = self.create_users_patterns()
        teacher, student = data['teacher'], data['student']
        
        self.create_classroom(student=student, teacher=teacher,day_of_class=self.tomorrow, start_time='12:00', number_of_hours=3)

        with self.assertRaises(ValidationError):
            self.create_classroom(student=student, teacher=teacher, day_of_class=self.tomorrow, start_time='12:30', number_of_hours=1)
            
    def test_if_price_fiel_is_correctly_defined(self):
        '''Testa se o campo price é definido corretamente'''
        data = self.create_users_patterns()
        teacher, student = data['teacher'], data['student']
        classroom = self.create_classroom(student=student, teacher=teacher, day_of_class=self.tomorrow, start_time='12:00', number_of_hours=3)
        price = teacher.hourly_price * classroom.number_of_hours
        self.assertEqual(classroom.price, price)
        
    def test_if_end_time_field_is_correctly_defined(self):
        '''Testa se o campo end_time é definido corretamente'''
        data = self.create_users_patterns()
        teacher, student = data['teacher'], data['student']
        classroom = self.create_classroom(student=student, teacher=teacher, day_of_class=self.tomorrow, start_time='12:00', number_of_hours=3)
        start_datetime = datetime.combine(classroom.day_of_class, classroom.start_time)
        end_datetime = start_datetime + timedelta(hours=classroom.number_of_hours)

        # Extrai o horário de término
        end_time = end_datetime.time()
        self.assertEqual(classroom.end_time, end_time)
            
    def test_checks_whether_a_validation_error_is_raised_if_the_class_tries_to_be_scheduled_on_the_same_day(self):
        '''Testa se lança um erro de validação se a aula tentar ser agendada no mesmo dia'''
        data = self.create_users_patterns()
        teacher, student = data['teacher'], data['student']
        with self.assertRaises(ValidationError):
            self.create_classroom(student=student, teacher=teacher, day_of_class=self.today, start_time='12:00', number_of_hours=1)
            
    def test_checks_whether_a_validation_error_is_raised_if_the_class_duration_is_zero(self):
        '''Testa se lança um erro de validação se a duração da aula for zero'''
        data = self.create_users_patterns()
        teacher, student = data['teacher'], data['student']
        with self.assertRaises(ValidationError):
            self.create_classroom(student=student, teacher=teacher, day_of_class=self.tomorrow, start_time='12:00', number_of_hours=0)
            
    def test_checks_whether_a_validation_error_is_raised_if_the_class_duration_is_negative(self):
        '''Testa se lança um erro de validação se a duração da aula for negativa'''
        data = self.create_users_patterns()
        teacher, student = data['teacher'], data['student']
        with self.assertRaises(ValidationError):
            self.create_classroom(student=student, teacher=teacher, day_of_class=self.tomorrow, start_time='12:00', number_of_hours=-1)