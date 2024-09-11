from rest_framework import serializers
from accounts.models import Student
from accounts.serializers import UserSerializer
from collections import defaultdict
from utils import verificar_email_valido
from accounts.models import User
import re

class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, source='user.email')
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    nome = serializers.CharField(required=True, source='name')
    foto = serializers.ImageField(required=False, source="profile_image")
    
    class Meta:
        model = Student
        fields = ['id', 'nome', 'password', 'password_confirmation', 'email', 'foto']
        
    def validate(self, data):
        email = data.get('user', {}).get('email', None)
        name = data.get('name')
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        errors = defaultdict(list)
        
        # Verificar senhas
        if password.strip() == '' or password is None:
            errors["password"].append("O campo password é obrigatório")
        if password_confirmation.strip() == '' or password_confirmation is None:
            errors["password_confirmation"].append("O campo password_confirmation é obrigatório")
        if password != password_confirmation:
            errors["password"].append("As senhas não coincidem.")
            
        # Validação de força da senha
        if len(password) < 8:
            errors["password"].append("A senha deve ter no mínimo 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            errors["password"].append("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[a-z]', password):
            errors["password"].append("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r'[0-9]', password):
            errors["password"].append("A senha deve conter pelo menos um número.")
        if not re.search(r'[@#$%^&+=]', password):
            errors["password"].append("A senha deve conter pelo menos um caractere especial (@, #, $, %, etc.).")
        
        if not name or name.isnumeric():
            errors["nome"].append("O nome não pode ser vazio e não pode ser apenas números.")
        if len(name) < 3:
            errors["nome"].append("O nome deve ter no mínimo 3 caracteres.")
        if len(name) > 255:
            errors["nome"].append("O nome deve ter no máximo 255 caracteres.")
        
        if User.objects.filter(email=email).exists():
            errors["email"].append("O email já está em uso")
        if not verificar_email_valido(email) and email is not None:
            errors["email"].append("Insira um email válido")
        
        if errors:
            raise serializers.ValidationError(errors)
            
        return super().validate(data)

    def create(self, validated_data):
        email = validated_data.pop('user', {}).pop('email', None)
        password =  validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')
        
        user_data = {"email": email, "password": password, "password_confirmation": password_confirmation, "is_student": True}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user =user_serializer.save()
        
        student = Student.objects.create(user=user, **validated_data)
        
        return student
    
    def update(self, instance, validated_data):
        email = validated_data.pop('user', {}).pop('email', instance.user.email)
        print(email)
        password = validated_data.pop('password', None)
        name = validated_data.pop('name', instance.name)
        profile_image = validated_data.pop('profile_image', instance.profile_image)
        
        instance.user.email = email
        if password:
            instance.user.set_password(password)
        instance.user.save()
        
        instance.name = name
        instance.profile_image = profile_image
        instance.save()
        
        return instance
    
    
class StudentProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=True, source='profile_image', write_only=True)
    
    class Meta:
        model = Student
        fields = ["foto"]