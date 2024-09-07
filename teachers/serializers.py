from rest_framework import serializers
from .models import Teacher, Subject
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name", "code")
        
    def validate(self, attrs):
        code = attrs.get('code')
        name = attrs.get('name')

        if not code.isalpha():
            raise serializers.ValidationError({"code": "O código deve conter apenas letras."})
        
        if not name or name.isdigit():
            raise serializers.ValidationError({"name": "O nome deve ser um texto válido e não pode ser apenas números."})

        if not code.isupper():
            raise serializers.ValidationError({"code": "O código deve conter todas as letras maiúsculas."})

        return super().validate(attrs)
        

class TeacherSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(
        source='name', required=True, min_length=3, max_length=100
    )
    email = serializers.EmailField(
        required=True, max_length=255
    )
    idade = serializers.IntegerField(
        source='age', required=True, min_value=18, max_value=100
    )
    descricao = serializers.CharField(
        source='description', required=True, min_length=10, max_length=500
    )
    valor_hora = serializers.DecimalField(
        source='hourly_price', required=True, min_value=Decimal(10.0), max_value=Decimal(500.0), max_digits=5, decimal_places=2
    )
    password_confirmation = serializers.CharField(
        write_only=True, required=True, min_length=6, max_length=128
    )
    foto_perfil = serializers.ImageField(read_only=True, source="profile_image")
    subjects_objects = SubjectSerializer(
        many=True,
        read_only=True,
        source="subjects"
    )
    
    class Meta:
        model = Teacher
        fields = (
            "id", "nome", "email", "idade", "descricao",
            "valor_hora", "foto_perfil", "created_at", "updated_at",
            "password", "password_confirmation", "subjects", "subjects_objects"
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "subjects": {"write_only": True}
        }
        
    def validate_password_confirmation(self, value):
        if self.initial_data.get('password') != value:
            raise serializers.ValidationError("As senhas não conferem")
        return value
    
    def validate_email(self, value):
        if Teacher.objects.filter(email=value).exists():
            raise serializers.ValidationError("Já existe um usuário com este e-mail")
        return value
    
    def create(self, validated_data):
        del validated_data['password_confirmation']
        validated_data['password'] = make_password(validated_data['password'])
        teacher = super().create(validated_data)
        return teacher
        
    def update(self, instance, validated_data):
        del validated_data['password_confirmation']
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        teacher = super().update(instance, validated_data)
        return teacher
    

class TeacherProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(
        required=True, write_only=True, source="profile_image"
    )

    class Meta:
        model = Teacher
        fields = ("foto",)
        