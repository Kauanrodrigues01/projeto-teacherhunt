from rest_framework import status
from accounts.models import Student
from .base.test_base_student import StudentTestBase

class TeacherListTests(StudentTestBase):
    def test_post_student(self): # 4.95s
        data = {
            "nome": "Jane Doe",
            "email": "jane@example.com",
            "password": "@Password1234",
            "password_confirmation": "@Password1234"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(name=data["nome"]).exists())

    def test_put_student(self): # 5.00s
        token = self.obtain_token()
        data = {
            "nome": "John Smith",
            "email": "putemail@gmail.com",
            "password": "@Putpassword1234",
            "password_confirmation": "@Putpassword1234"
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.student.refresh_from_db()
        self.student.user.refresh_from_db()
        self.assertEqual(self.student.name, data['nome'])
        self.assertEqual(self.student.user.email, data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_put_student(self):
        token = self.obtain_token()
        data = {
            "nome": "John Smith"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(self.url, data, format='json')
        self.student.refresh_from_db()
        self.student.user.refresh_from_db()
        self.assertEqual(self.student.name, data['nome'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_delete_student(self):
        # 4.76s
        token = self.obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())
    
    # def test_partial_update_just_password_put_teacher(self):
    #     token = self.obtain_token()
    #     data = {
    #         "password": "@NewPassword1234",
    #         "password_confirmation": "@Newpassword1234"
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    #     response = self.client.put(self.url, data, format='json')
    #     self.teacher.refresh_from_db()
    #     self.teacher.user.refresh_from_db()
    #     token = self.obtain_token(password=data['password'])
    #     if token == False:
    #        self.fail('Password not updated')
    #     self.assertTrue(True)
    
    # def test_partial_update_just_email_put_teacher(self):
    #     token = self.obtain_token()
    #     data = {
    #         "email": "testputemail@gamil.com"
    #     }
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    #     self.client.put(self.url, data, format='json')
    #     self.teacher.refresh_from_db()
    #     self.teacher.user.refresh_from_db()
    #     self.assertEqual(self.teacher.user.email, data['email'])

