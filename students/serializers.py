from rest_framework import serializers
from accounts.models import Student, Rating, Teacher
from accounts.serializers import UserSerializer
from collections import defaultdict
from utils import verify_email
from accounts.models import User
import re

class StudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, source='user.email')
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    nome = serializers.CharField(required=False, source='name')
    foto = serializers.ImageField(required=False, source='profile_image')
    
    class Meta:
        model = Student
        fields = ['id', 'nome', 'password', 'password_confirmation', 'email', 'foto']
        
    def validate(self, data):
        email = data.get('user', {}).get('email', None)
        name = data.get('name')
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        errors = defaultdict(list)
        request_method = self.context.get('request_method')
        pattern = r'^[a-zA-Z]+$'
        
        if request_method == 'PUT':
            if self.instance:
                email = email or None
                name = name or self.instance.name
                password = password or None
                password_confirmation = password_confirmation or None
        
        if password is None and password_confirmation is None and request_method == 'POST':
            errors['password'].append('O campo password é obrigatório')
            errors['password_confirmation'].append('O campo password_confirmation é obrigatório')
        if password is not None or password_confirmation is not None and request_method == 'POST':
            if password.strip() == '' or password is None:
                errors['password'].append('O campo password é obrigatório')
            if password_confirmation.strip() == '' or password_confirmation is None:
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

        name_list = name.split(' ')
        errors_name_list = 0
        for name in name_list:
            if not re.match(pattern, name):
                errors_name_list += 1
        if errors_name_list > 0:
            errors['nome'].append('O nome deve conter apenas letras.')
        if len(name) < 3:
            errors['nome'].append('O nome deve ter no mínimo 3 caracteres.')
        if len(name) > 100:
            errors['nome'].append('O nome deve ter no máximo 100 caracteres.')
        
        if User.objects.filter(email=email).exists():
            errors['email'].append('Este email já está cadastrado')
        if not verify_email(email) and email is not None:
            errors['email'].append('Insira um email válido')
        
        if errors:
            raise serializers.ValidationError(errors)
            
        return super().validate(data)

    def create(self, validated_data):
        email = validated_data.pop('user', {}).pop('email', None)
        password =  validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')
        
        user_data = {'email': email, 'password': password, 'password_confirmation': password_confirmation, 'is_student': True}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user =user_serializer.save()
        
        student = Student.objects.create(user=user, **validated_data)
        
        return student
    
    def update(self, instance, validated_data):
        email = validated_data.pop('user', {}).pop('email', instance.user.email)
        if email != instance.user.email:
            instance.user.is_active = False
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
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['foto_perfil'] = data.pop('foto')
        data['created_at'] = instance.create_at
        data['updated_at'] = instance.update_at
        return data
    
    
class StudentProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=True, source='profile_image', write_only=True)
    
    class Meta:
        model = Student
        fields = ['foto']

class RatingSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), source='teacher')
    aluno = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student')
    avaliacao = serializers.FloatField(source='rating')
    comentario = serializers.CharField(source='comment')

    class Meta:
        model = Rating
        fields = ['id', 'professor', 'aluno', 'avaliacao', 'comentario']

    def validate(self, attrs):
        teacher = attrs.get('teacher', None)
        student = attrs.get('student',  None)
        rating = attrs.get('rating', None)
        comment = attrs.get('comment', None)
        errors = defaultdict(list)

        if teacher is None:
            errors['professor'].append('Este campo é obrigatório.')
        if student is None:
            errors['aluno'].append('Este campo é obrigatório.')
        if rating is None:
            errors['avaliacao'].append('Este campo é obrigatório.')

        if not Teacher.objects.filter(id=teacher.id).exists():
            errors['professor'].append('Professor não encontrado.')
        if Rating.objects.filter(teacher=teacher, student=student).exists():
            errors['detail'].append('Você já avaliou este professor.')
        if rating is not None:
            if not isinstance(rating, int) and not isinstance(rating, float):
                errors['avaliacao'].append('A nota deve ser um número.') 
            if rating < 0 or rating > 5:
                errors['avaliacao'].append('A nota deve ser um valor entre 0 e 5.')
        if comment is not None:
            if not isinstance(comment, str):
                errors['comentario'].append('O comentário deve ser uma string.')
            if len(comment) < 10:
                errors['comentario'].append('O comentário deve ter no mínimo 10 caracteres.')
            if len(comment) > 500:
                errors['comentario'].append('O comentário deve ter no máximo 500 caracteres.')
            if comment.isnumeric():
                errors['comentario'].append('O comentário não pode ser apenas números.')
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        teacher = validated_data.pop('teacher')
        student = validated_data.pop('student')
        rating = validated_data.pop('rating')
        comment = validated_data.pop('comment')
        
        rating = Rating.objects.create(teacher=teacher, student=student, rating=rating, comment=comment)
        
        return rating
    
    def to_representation(self, instance):
        professor = instance.teacher
        aluno = instance.student
        aluno_nome = aluno.name
        professor_nome = professor.name
        avaliacao = instance.rating
        comentario = instance.comment

        data = {
            'professor': professor_nome,
            'aluno': aluno_nome,
            'avaliacao': avaliacao,
            'comentario': comentario
        }

        return data
    