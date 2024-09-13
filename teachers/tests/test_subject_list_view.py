from .base.test_base_teacher_view import TeacherTestBase
from django.urls import reverse

class TestTeacherListForSubjectsView(TeacherTestBase):
    def test_read_all_subjects(self):
        response = self.client.get(reverse('teachers:subjects-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Math')
