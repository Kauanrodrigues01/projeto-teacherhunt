from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, Teacher, Subject
from rest_framework.exceptions import ErrorDetail

class AccountsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('teachers:list')

        # Criar um usuário
        self.user = User.objects.create_user(email='teacher@example.com', password='@Password1234', is_teacher=True, is_active=True)
        self.teacher = Teacher.objects.create(
            user=self.user,
            name='John Doe',
            description='A nice teacher',
            hourly_price=50.00,
            age=30
        )
        self.subject = Subject.objects.create(name='Math')
        
    def login(self):
        login_url = reverse('accounts:login')
        response = self.client.post(login_url, {
            'email': 'teacher@example.com',
            'password': '@Password1234'
        })
        return response
    
    def refresh(self, refresh_token):
        refresh_url = reverse('accounts:refresh')
        response = self.client.post(refresh_url, {
            'refresh_token': refresh_token
        })
        return response
    
    def logout(self, refresh_token):
        refresh_url = reverse('accounts:logout')
        response = self.client.post(refresh_url, {
            'refresh_token': refresh_token
        })
        return response
        
    def test_obtain_token_and_refresh_token_in_login(self):
        response = self.login()
        if 'token' not in response.data:
            self.fail('Token not found in response')
        if 'refresh_token' not in response.data:
            self.fail('Refresh token not found in response')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('refresh_token', response.data)
    
    def test_obtain_token_and_refresh_token_in_refresh(self):
        response_login = self.login()
        refresh_token = response_login.data['refresh_token']
        
        response_refresh = self.refresh(refresh_token)
        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn('token', response_refresh.data)
        self.assertIn('refresh_token', response_refresh.data)  
        
    def test_logout(self):
        response_login = self.login()
        refresh_token = response_login.data['refresh_token']
        
        response_logout = self.logout(refresh_token)
        response_attempt_refresh = self.refresh(refresh_token)
        self.assertEqual(response_logout.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response_attempt_refresh.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_attempt_refresh.data, {'detail': 'Token está na blacklist', 'code': 'token_not_valid'})
        
        