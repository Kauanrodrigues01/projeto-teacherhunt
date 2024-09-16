from django.urls import reverse
from rest_framework import status
from classroom.models import Classroom
from .base.test_base_student_create_classroom import TestBaseCreateClassroomView
from datetime import datetime
from accounts.models import User, Teacher, Student

class StudentCreateClassroomView(TestBaseCreateClassroomView):
    def test_create_classroom(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        data_objeto = datetime.strptime(self.data['dia_da_aula'], '%Y-%m-%d')
        data_formatada = data_objeto.strftime('%d/%m/%Y')
        horario_objeto = datetime.strptime(self.data['horario_de_inicio'], '%H:%M').time()
        horario_formatado = horario_objeto.strftime('%H:%M:%S')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['professor'], self.data['professor'])
        self.assertEqual(response.data['dia_da_aula'], data_formatada)
        self.assertEqual(response.data['horario_de_inicio'], horario_formatado)
        self.assertEqual(response.data['numero_de_horas'], self.data['numero_de_horas'])
        self.assertEqual(response.data['descricao_da_aula'], self.data['descricao_da_aula'])
        self.assertTrue(Classroom.objects.filter(id=response.data['id']).exists())

    def test_create_classroom_without_description(self):
        del self.data['descricao_da_aula']
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        data_objeto = datetime.strptime(self.data['dia_da_aula'], '%Y-%m-%d')
        data_formatada = data_objeto.strftime('%d/%m/%Y')
        horario_objeto = datetime.strptime(self.data['horario_de_inicio'], '%H:%M').time()
        horario_formatado = horario_objeto.strftime('%H:%M:%S')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['professor'], self.data['professor'])
        self.assertEqual(response.data['dia_da_aula'], data_formatada)
        self.assertEqual(response.data['horario_de_inicio'], horario_formatado)
        self.assertEqual(response.data['numero_de_horas'], self.data['numero_de_horas'])
        self.assertTrue(Classroom.objects.filter(id=response.data['id']).exists())

    def test_create_classroom_with_description_about_class_just_numbers(self):
        self.data['descricao_da_aula'] = '1234    56789    10'
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['descricao_da_aula'][0], 'A descrição da aula não pode conter apenas números.')

    def test_create_classroom_with_description_about_class_less_than_10(self):
        self.data['descricao_da_aula'] = '     a' * 9
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['descricao_da_aula'][0], 'A descrição da aula deve ter mais de 10 caracteres.')

    def test_if_an_error_arises_when_trying_to_create_a_classroom_without_a_teacher(self):
        del self.data['professor']
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['professor'][0], 'Este campo é obrigatório.')

    def test_if_an_error_arises_when_trying_to_create_a_classroom_without_a_day_of_class(self):
        del self.data['dia_da_aula']
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['dia_da_aula'][0], 'Este campo é obrigatório.')

    def test_if_an_error_arises_when_trying_to_create_a_classroom_without_a_start_time(self):
        del self.data['horario_de_inicio']
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['horario_de_inicio'][0], 'Este campo é obrigatório.')

    def test_if_an_error_arises_when_trying_to_create_a_classroom_without_a_number_of_hours(self):
        del self.data['numero_de_horas']
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['numero_de_horas'][0], 'Este campo é obrigatório.')

    def test_if_an_error_arises_when_to_create_a_classroom_with_number_of_hours_greater_than_4_hours(self):
        self.data['numero_de_horas'] = 5
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['numero_de_horas'][0], 'O número de horas deve ser menor que 5.')

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_teacher_with_an_empty_string(self):
        self.data['professor'] = ''
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['professor'][0], 'Este campo não pode ser nulo.')

    def test_whether_an_error_occurs_when_trying_to_create_a_classroom_with_day_of_class_with_an_empty_string(self):
        self.data['dia_da_aula'] = ''
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['dia_da_aula'][0], 'Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.')

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_start_time_with_an_empty_string(self):
        self.data['horario_de_inicio'] = ''
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['horario_de_inicio'][0], 'Formato inválido para Tempo. Use um dos formatos a seguir: hh:mm[:ss[.uuuuuu]].')

    def test_whether_to_create_classrooms_with_a_time_of_19_30(self):
        self.data['horario_de_inicio'] = '19:30'
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_an_end_time_greater_than_21_00(self):
        '''
        end_time = start_time + number_of_hours
        '''
        self.data['horario_de_inicio'] = '20:30'
        self.data['numero_de_horas'] = 2
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'][0], 'O Hórario de termino não deve exceder 21:00.')

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_an_invalid_start_time(self):
        self.data['horario_de_inicio'] = '20:35'
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['horario_de_inicio'][0], 'Horário inválido. Os horários permitidos são de 07:00 até 20:00 com um intervalo de uma meia hora.')

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_number_of_hours_with_an_empty_string(self):
        self.data['numero_de_horas'] = ''
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['numero_de_horas'][0], 'Um número inteiro válido é exigido.')

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_teacher_with_a_negative_number(self):
        self.data['professor'] = -1
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_number_of_hours_with_a_negative_number_or_zero(self):
        self.data['numero_de_horas'] = -1
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['numero_de_horas'][0], 'O número de horas deve ser maior que 0.')

        self.data['numero_de_horas'] = 0
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['numero_de_horas'][0], 'O número de horas deve ser maior que 0.')

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_teacher_that_already_has_a_class_scheduled_for_the_same_day_and_time(self):
        self.client.post(self.url, self.data, format='json')
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response1 = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Classroom.objects.filter(id=response1.data['id']).exists())
        response2 = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data['error'][0], 'O estudante já tem uma aula marcada nesse horário.')

    def test_if_an_error_occurs_when_trying_to_create_a_classroom_with_teacher_that_already_has_a_class_scheduled_for_the_same_day_and_time_with_another_student(self):
        user2_student = User.objects.create_user(email='userstudent2@example.com', password='@Password1234',)
        student2 = Student.objects.create(user=user2_student, name='Student Teste 2')
        classroom = Classroom.objects.create(
            teacher=self.teacher,
            student=student2,
            day_of_class=self.data['dia_da_aula'],
            start_time=self.data['horario_de_inicio'],
            number_of_hours=1,
            description_about_class='Aula de teste'
        )

        self.data['aluno'] = self.student.id
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response2 = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data['error'][0], 'O professor já tem uma aula marcada nesse horário.')
        self.assertFalse(Classroom.objects.filter(student=self.data['aluno'], teacher=self.data['professor']).exists())

    def test_whether_an_error_occurs_when_trying_to_create_a_classroom_with_a_student_who_already_has_a_class_scheduled_for_the_same_day_and_time_with_another_teacher(self):
        user_teacher2 = User.objects.create_user(
            email='userteacher2@example.com',
            password='@Password1234',
        )
        teacher2 = Teacher.objects.create(
            user=user_teacher2,
            name='Teacher Teste 2',
            age=30,
            description='Description teacher',
            hourly_price=50.00
        )
        classroom = Classroom.objects.create(
            teacher=teacher2,
            student=self.student,
            day_of_class=self.data['dia_da_aula'],
            start_time=self.data['horario_de_inicio'],
            number_of_hours=1,
            description_about_class='Aula de teste'
        )

        self.data['professor'] = self.teacher.id
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response2 = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data['error'][0], 'O estudante já tem uma aula marcada nesse horário.')
        self.assertFalse(Classroom.objects.filter(teacher=self.data['professor'], student=self.student).exists())
