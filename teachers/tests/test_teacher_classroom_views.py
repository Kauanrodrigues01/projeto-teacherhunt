from .base.test_base_teacher_classroom import TeacherClassroomTestBase
from django.urls import reverse

class TestTeacherClassroomsViews(TeacherClassroomTestBase):
    def test_if_a_teacher_can_only_view_classes_related_to_them(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(reverse('teachers:teacher-classrooms'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['id'], self.classroom.id)
        self.assertEqual(response.data[1]['id'], self.classroom_accepted.id)
        self.assertEqual(response.data[2]['id'], self.classroom_cancelled.id)

    def test_if_the_class_status_filter_is_working_correctly_from_the_teacher_view(self):
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
            response = self.client.get(reverse('teachers:teacher-classrooms'), {'status': status})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data[0]['status'], status.capitalize())
            self.assertEqual(response.data[0]['id'], id_classroom)
            self.assertEqual(len(response.data), 1)

    def test_if_a_teacher_can_view_the_classroom_detail_related_to_them(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(reverse('teachers:teacher-classroom-detail', kwargs={'pk': self.classroom.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.classroom.id)
        self.assertEqual(response.data['professor'], self.teacher.id)

    def test_if_a_teacher_cannot_view_the_classroom_detail_that_is_not_related_to_him(self):
        token = self.obtain_token(email='teacher2alternative@gmail.com', password='@Passwordteacher222')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(reverse('teachers:teacher-classroom-detail', kwargs={'pk': self.classroom.id}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'detail': 'Aula não encontrada'})

    def test_if_to_accept_a_class_correctly(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(reverse('teachers:teacher-accepted-classroom', kwargs={'pk': self.classroom.id}))
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.status, 'A')
        self.assertEqual(response.status_code, 200)

    def test_if_to_cancel_a_class_correctly(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(reverse('teachers:teacher-cancelled-classroom', kwargs={'pk': self.classroom.id}))
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.status, 'C')
        self.assertEqual(response.status_code, 200)

    def test_if_a_teacher_cannot_accept_a_class_that_is_not_related_to_him(self):
        token = self.obtain_token(email='teacher2alternative@gmail.com', password='@Passwordteacher222')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(reverse('teachers:teacher-accepted-classroom', kwargs={'pk': self.classroom.id}))
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.status, 'P')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'error': 'Você não tem permissão para aceitar essa aula.'})

    def test_if_a_teacher_cannot_cencel_a_class_that_is_not_related_to_him(self):
        token = self.obtain_token(email='teacher2alternative@gmail.com', password='@Passwordteacher222')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(reverse('teachers:teacher-cancelled-classroom', kwargs={'pk': self.classroom.id}))
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.status, 'P')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'error': 'Você não tem permissão para cancelar essa aula.'})

