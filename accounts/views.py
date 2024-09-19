from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework import generics
from .models import User


from accounts.serializers import RequestPasswordResetEmailSerializer, SetNewPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from utils import send_email, verify_email

# Create your views here.

class CustomTokenBlacklistView(TokenBlacklistView):

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_205_RESET_CONTENT)

class RequestPasswordResetEmail(generics.GenericAPIView):
    '''
    # Send request to reset password to the user's email
    '''
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    '''
    # Check if the token is valid
    '''
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
        
class SetNewPasswordAPI(generics.GenericAPIView):
    '''
    # Set new password
    '''

    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)