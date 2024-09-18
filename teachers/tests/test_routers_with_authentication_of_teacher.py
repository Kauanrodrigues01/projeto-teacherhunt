from .base.test_base_routes_with_or_without_authentication import TestBaseAuthentication
from django.urls import reverse

class TestTeacherRoutesWithAuthentication(TestBaseAuthentication):
    '''
    This class of test, tests the routes that require authentication as a teacher.
    '''
    # Test route to update teacher
    def testi_if_a_401_status_code_is_returned_if_the_user_tries_to_access_the_put_teacher_route_without_authentication(self):
        response = self.client.put(reverse('teachers:list'))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_put_teacher_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(reverse('teachers:list'))
        self.assertEqual(403, response.status_code)

    # Test route to delete teacher
    def testi_if_a_401_status_code_is_returned_if_the_user_tries_to_access_the_delete_teacher_route_without_authentication(self):
        response = self.client.delete(reverse('teachers:list'))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_delete_teacher_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(reverse('teachers:list'))
        self.assertEqual(403, response.status_code)

    # Test route to upload teacher profile image
    def test_if_a_401_status_code_is_returned_if_the_user_tries_to_access_the_teacher_profile_image_upload_route_without_authentication(self):
        response = self.client.put(reverse('teachers:profile-image'))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_teacher_profile_image_upload_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(reverse('teachers:profile-image'))
        self.assertEqual(403, response.status_code)

    # Test route to get logged in teacher details
    def test_if_a_401_status_code_is_returned_if_the_user_tries_to_access_the_logged_in_teacher_details_route_without_authentication(self):
        response = self.client.get(reverse('teachers:me'))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_logged_in_teacher_details_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('teachers:me'))
        self.assertEqual(403, response.status_code)

    # Test route to get classrooms of teacher
    def test_if_a_401_status_code_is_returned_if_the_user_tries_to_access_the_teachers_class_route_without_authentication(self):
        response = self.client.get(reverse('teachers:teacher-classrooms'))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_teachers_class_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('teachers:teacher-classrooms'))
        self.assertEqual(403, response.status_code)

    def test_if_a_401_status_code_is_returned_if_the_user_tries_to_access_the_teachers_class_details_route_without_authentication(self):
        response = self.client.get(reverse('teachers:teacher-classroom-detail', kwargs={'pk': 1}))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_teachers_class_details_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('teachers:teacher-classroom-detail', kwargs={'pk': 1}))
        self.assertEqual(403, response.status_code)

    # Test route to accept a classroom
    def test_if_a_401_status_code_will_be_returned_if_the_user_attempts_to_access_the_accept_a_class_route_without_authentication(self):
        response = self.client.get(reverse('teachers:teacher-accepted-classroom', kwargs={'pk': 1}))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_accept_a_class_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('teachers:teacher-accepted-classroom', kwargs={'pk': 1}))
        self.assertEqual(403, response.status_code)

    # Test route to cancel a classroom
    def test_if_a_401_status_code_will_be_returned_if_the_user_attempts_to_access_the_cancel_a_class_route_without_authentication(self):
        response = self.client.get(reverse('teachers:teacher-cancelled-classroom', kwargs={'pk': 1}))
        self.assertEqual(401, response.status_code)

    def test_if_a_status_code_403_is_returned_if_the_user_tries_to_access_the_cancel_a_class_route_authenticated_as_a_student(self):
        token = self.obtain_token_student()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('teachers:teacher-cancelled-classroom', kwargs={'pk': 1}))
        self.assertEqual(403, response.status_code)