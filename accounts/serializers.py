from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        '''
        # Remove o "access" e cria um novo campo dentro de data e salva o "access"
        
        # Remove o "refresh" e cria um novo campo dentro de data e salva o "refresh"
        '''
        data = super().validate(attrs)
        data['token'] = data.pop("access")
        data['refresh_token'] = data.pop('refresh')
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh_token = serializers.CharField(required=True)
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = attrs.pop("refresh_token")
        data = super().validate(attrs)
        data["token"] = data.pop("access")
        data["refresh_token"] = data.pop("refresh")
        return data


class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    refresh_token = serializers.CharField(required=True)
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = attrs.pop("refresh_token")
        return super().validate(attrs)
    