from django.urls import reverse
from .base.test_base_student_view import StudentTestBase

class StudentTestMeView(StudentTestBase):
    def test_if_the_data_of_the_logged_in_student_is_returned(self):
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(reverse('students:me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.student.id)
        self.assertEqual(response.data['nome'], self.student.name)
        self.assertEqual(response.data['email'], self.student.user.email)