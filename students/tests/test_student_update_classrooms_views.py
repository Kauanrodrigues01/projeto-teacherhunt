from .base.test_base_student_classroom import StudentClassroomTestBase
from django.urls import reverse
from datetime import timedelta
from datetime import datetime

class TestStudentUpdateClassroomsViews(StudentClassroomTestBase):
    def test_update_all_fields_in_the_class(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data={ 
            'dia_da_aula': self.tomorrow + timedelta(days=1),
            'horario_de_inicio': '14:00',
            'numero_de_horas': 2,
            'descricao_da_aula': 'Aula de teste atulizada'
        }

        response = self.client.put(reverse('students:student-update-classroom', kwargs={'pk': self.classroom.id}), data=data)
        data['horario_de_inicio'] = datetime.strptime(data['horario_de_inicio'], "%H:%M").time()
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.day_of_class, data['dia_da_aula'])
        self.assertEqual(self.classroom.start_time, data['horario_de_inicio'])
        self.assertEqual(self.classroom.number_of_hours, data['numero_de_horas'])
        self.assertEqual(self.classroom.description_about_class, data['descricao_da_aula'])
        self.assertEqual(response.status_code, 200)

    def test_if_student_cannot_update_class_that_is_not_related_to_them(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data={ 
            'dia_da_aula': self.tomorrow + timedelta(days=1),
            'horario_de_inicio': '14:00',
            'numero_de_horas': 2,
            'descricao_da_aula': 'Aula de teste atulizada'
        }

        response = self.client.put(reverse('students:student-update-classroom', kwargs={'pk': self.classroom_alternative.id}), data=data)
        self.classroom_alternative.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'error': 'Você não tem permissão para alterar esta aula.'})

    def test_update_only_day_of_class_in_the_class(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data={ 
            'dia_da_aula': self.tomorrow + timedelta(days=1)
        }

        response = self.client.put(reverse('students:student-update-classroom', kwargs={'pk': self.classroom.id}), data=data)
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.day_of_class, data['dia_da_aula'])
        self.assertEqual(response.status_code, 200)

    def test_update_only_start_time_in_the_class(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data={ 
            'horario_de_inicio': '19:00',
        }

        response = self.client.put(reverse('students:student-update-classroom', kwargs={'pk': self.classroom.id}), data=data)
        data['horario_de_inicio'] = datetime.strptime(data['horario_de_inicio'], "%H:%M").time()
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.start_time, data['horario_de_inicio'])
        self.assertEqual(response.status_code, 200)

    def test_update_only_number_of_hours_in_the_class(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data={ 
            'numero_de_horas': 2,
        }

        response = self.client.put(reverse('students:student-update-classroom', kwargs={'pk': self.classroom.id}), data=data)
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.number_of_hours, data['numero_de_horas'])
        self.assertEqual(response.status_code, 200)

    def test_update_only_description_about_class_in_the_class(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data={ 
            'descricao_da_aula': 'descrição de teste atualizada'
        }

        response = self.client.put(reverse('students:student-update-classroom', kwargs={'pk': self.classroom.id}), data=data)
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.description_about_class, data['descricao_da_aula'])
        self.assertEqual(response.status_code, 200)
