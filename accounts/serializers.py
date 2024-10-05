import django.core.validators
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer
from rest_framework import serializers
from .models import Student, Teacher, User
from collections import defaultdict

# redefining the password reset serializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from utils import send_email, verify_email

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        '''
        # Remove o "access" e cria um novo campo dentro de data e salva o "access"
        
        # Remove o "refresh" e cria um novo campo dentro de data e salva o "refresh"
        '''
        data = super().validate(attrs)
        data['token'] = data.pop('access')
        data['refresh_token'] = data.pop('refresh')
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh_token = serializers.CharField(required=True)
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = attrs.pop('refresh_token')
        data = super().validate(attrs)
        data['token'] = data.pop('access')
        data['refresh_token'] = data.pop('refresh')
        return data

class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    refresh_token = serializers.CharField(required=True)
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = attrs.pop('refresh_token')
        return super().validate(attrs)
    

class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    is_teacher = serializers.BooleanField(required=False)
    is_student = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirmation', 'is_teacher', 'is_student']

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('As senhas não coincidem.')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
    
class RequestPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')

        if not verify_email(email):
            raise serializers.ValidationError({'email': 'Email inválido'})
        
        if User.objects.filter(email=email).exists():

            user = User.objects.get(email=email)
            if user.is_student:
                student = Student.objects.get(user=user)
                username = student.name
            else:
                teacher = Teacher.objects.get(user=user)
                username = teacher.name

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(self.context['request']).domain
            relative_link = reverse('accounts:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = f'http://{current_site}{relative_link}'
            email_body = f'Hi, {username} \n Use the link below to reset your password \n {absurl}'

            send_email('Reset your Password', email_body, user.email)
        else:
            raise serializers.ValidationError({'email': 'Email não encontrado'})

        return super().validate(attrs)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField( write_only=True)
    password_confirmation = serializers.CharField( write_only=True)
    uidb64 = serializers.CharField(min_length=1 ,write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'password_confirmation', 'uidb64', 'token']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        errors = defaultdict(list)

        if password.strip() == '':
            errors['password'].append('O campo password é obrigatório')
        if password_confirmation.strip() == '':
            errors['password_confirmation'].append('O campo password_confirmation é obrigatório')
        if password != password_confirmation:
            errors['password'].append('As senhas não conferem.')
    
        # Validação de força da senha
        if len(password) < 8:
            errors['password'].append('A senha deve ter no mínimo 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            errors['password'].append('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[a-z]', password):
            errors['password'].append('A senha deve conter pelo menos uma letra minúscula.')
        if not re.search(r'[0-9]', password):
            errors['password'].append('A senha deve conter pelo menos um número.')
        if not re.search(r'[@#$%^&+=]', password):
            errors['password'].append('A senha deve conter pelo menos um caractere especial (@, #, $, %, etc.).')

        if errors:
            raise serializers.ValidationError(errors)

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({'token': 'Token inválido, solicite um novo.'})

            user.set_password(password)
            user.save()
            return user
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError({'token': 'Token inválido, solicite um novo.'})

class SendRequestEmailActiveUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')

        if not verify_email(email):
            raise serializers.ValidationError({'email': 'Email inválido'})
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                raise serializers.ValidationError({'email': 'Conta já ativada.'})
            if user.is_student:
                student = Student.objects.get(user=user)
                username = student.name
            else:
                teacher = Teacher.objects.get(user=user)
                username = teacher.name

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(self.context['request']).domain
            relative_link = reverse('accounts:active-user', kwargs={'uidb64': uidb64, 'token': token})
            absurl = f'http://{current_site}{relative_link}'
            email_body = f'Hi, {username} \n Use the link below to active account \n {absurl}'

            send_email('Ativar conta', email_body, user.email)
        else:
            raise serializers.ValidationError({'email': 'Email não encontrado'})

        return super().validate(attrs)

