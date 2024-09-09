from rest_framework import serializers
from accounts.models import Student
from accounts.serializers import UserSerializer
from collections import defaultdict
from utils import verificar_email_valido
import re

class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, source='user.email')
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    nome = serializers.CharField(required=True, source='name')

    class Meta:
        model = Student
        fields = ['id', 'nome', 'password', 'password_confirmation', 'email']
        
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
            
        if not verificar_email_valido(email):
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
        password = validated_data.pop('password', None)
        name = validated_data.pop('name', instance.name)
        
        instance.user.email = email
        instance.name = name
        if password:
            instance.user.set_password(password)
        instance.save()
        
        return instance

# class ClassroomSerializer(serializers.ModelSerializer):
#     student_name = serializers.CharField(source='student.name', read_only=True)
#     teacher_name = serializers.CharField(source='teacher.name', read_only=True)

#     class Meta:
#         model = Classroom
#         fields = ['id', 'student', 'teacher', 'student_name', 'teacher_name', 'created_at', 'updated_at']
#         extra_kwargs = {
#             'created_at': {'read_only': True},
#             'updated_at': {'read_only': True}
#         }

#     def validate(self, data):
#         student = data.get('student')
#         teacher = data.get('teacher')

#         # Validação para garantir que a mesma combinação de aluno e professor não exista
#         if Classroom.objects.filter(student=student, teacher=teacher).exists():
#             raise serializers.ValidationError('Já existe uma aula agendada entre este aluno e este professor.')

#         return data