from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer
from rest_framework import serializers
from .models import User

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