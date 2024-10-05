from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework import generics
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView


from accounts.serializers import RequestPasswordResetEmailSerializer, SetNewPasswordSerializer, SendRequestEmailActiveUserSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import NotAuthenticated

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Token view to handle inactive users.
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"detail": "Sua conta ainda não foi ativada. Por favor, verifique seu e-mail para ativar sua conta."}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)

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
        return Response({'sucesso': 'Foi enviado um email com o link de redefinição de senha.'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    '''
    # Check if the token is valid
    '''
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise NotAuthenticated({'error': 'Token inválido, solicite um novo.'})

            return Response({'message': 'Credenciais válidas', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            raise NotAuthenticated({'error': 'Token inválido, solicite um novo.'})
        
class SetNewPasswordAPI(generics.GenericAPIView):
    '''
    # Set new password
    '''

    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Senha redefinida com sucesso.'}, status=status.HTTP_200_OK)
    

class SendRequestEmailActiveUser(generics.GenericAPIView):
    serializer_class = SendRequestEmailActiveUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Email enviado com sucesso.'}, status=status.HTTP_200_OK)
    
class ActiveUser(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise NotAuthenticated({'error': 'Token inválido, solicite um novo.'})
            
            user.is_active = True
            user.save()
            return Response({'message': 'Conta ativada com sucesso!'})
        except DjangoUnicodeDecodeError as identifier:
            raise NotAuthenticated({'error': 'Token inválido, solicite um novo.'})