from .base.test_base_student_classroom import StudentClassroomTestBase
from django.urls import reverse

class TestTeacherClassroomsViews(StudentClassroomTestBase):
    def test_if_a_student_can_only_view_classes_related_to_them(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(reverse('students:student-classrooms'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.student.classrooms.count()) # Aplicar nos testes de teachers
        self.assertEqual(len(response.data), 3) 
        self.assertEqual(response.data[0]['id'], self.classroom.id)
        self.assertEqual(response.data[1]['id'], self.classroom_accepted.id)
        self.assertEqual(response.data[2]['id'], self.classroom_cancelled.id)

    def test_if_the_class_status_filter_is_working_correctly_from_the_student_view(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        status_mapping =[
            {'status': 'pendente', 'id_classroom': self.classroom.id},
            {'status': 'aceita', 'id_classroom': self.classroom_accepted.id},
            {'status': 'cancelada', 'id_classroom': self.classroom_cancelled.id}
        ]
        for status_dic in status_mapping:
            status = status_dic['status']
            id_classroom = status_dic['id_classroom']
            response = self.client.get(reverse('students:student-classrooms'), {'status': status})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data[0]['status'], status.capitalize())
            self.assertEqual(response.data[0]['id'], id_classroom)
            self.assertEqual(len(response.data), 1)

    def test_if_a_student_can_view_the_classroom_detail_related_to_them(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(reverse('students:student-classroom-detail', kwargs={'pk': self.classroom.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.classroom.id)
        self.assertEqual(response.data['aluno'], self.student.id)

    def test_if_a_student_cannot_view_the_classroom_detail_that_is_not_related_to_him(self):
        token = self.obtain_token(email='Student2alternative@gmail.com', password='@PasswordStudent222')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(reverse('students:student-classroom-detail', kwargs={'pk': self.classroom.id}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'Aula não encontrada'})
    