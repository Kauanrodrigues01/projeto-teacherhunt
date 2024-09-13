from django.urls import reverse
from .base.test_base_teacher_view import TeacherTestBase
from accounts.models import User, Teacher, Subject
from ..serializers import TeacherSerializer

class TestTeacherListForSubjectsView(TeacherTestBase):
    def test_filter_teachers_by_students(self):
        user2 = User.objects.create_user(email='teacher2@example.com', password='@Password1234', is_teacher=True)
        subject2 = Subject.objects.create(name='Portuguese')
        teacher2 = Teacher.objects.create(
            user=user2,
            name='John Vick',
            description='A nice teacher',
            hourly_price=20.00,
            age=45,
        )
        teacher2.subjects.add(subject2)
        teacher2.save()
        teacher2_serializer = TeacherSerializer(teacher2)
        self.teacher.subjects.add(self.subject)
        self.teacher.save()

        response = self.client.get(reverse('teachers:list-for-subject', kwargs={'pk':1}))
        response_data = response.data
        teacher2_serializer_data = teacher2_serializer.data
        if isinstance(response_data, dict):
            response_data = [response_data]
        self.assertNotIn(teacher2_serializer_data, response_data)