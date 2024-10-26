from rest_framework import serializers
from accounts.models import Teacher, Subject, Rating, User
from accounts.serializers import UserSerializer
from collections import defaultdict
from utils import verify_email, round_rating
import re
from django.db import models

class SubjectSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True, max_length=255, source='name')
    class Meta:
        model = Subject
        fields = ('id', 'nome')
        
    def validate(self, attrs):
        name = attrs.get('name')
        
        if not name or name.isdigit():
            raise serializers.ValidationError({'nome': 'O nome deve ser um texto válido e não pode ser apenas números.'})
        
        if Subject.objects.filter(name=name).exists():
            raise serializers.ValidationError({'nome': 'Já existe esta matéria'})

        return super().validate(attrs)
        

class TeacherSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True, source='name')
    email = serializers.EmailField(required=True, source='user.email')
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    descricao = serializers.CharField(required=True, source='description')
    idade = serializers.IntegerField(required=True, source='age')
    valor_hora = serializers.DecimalField(required=True, source='hourly_price', max_digits=6, decimal_places=2)
    materias = serializers.ListField(child=serializers.IntegerField(), required=True, source='subjects')
    materias_objetos = SubjectSerializer(many=True, source='subjects', read_only=True)
    foto = serializers.ImageField(required=False, source='profile_image')

    class Meta:
        model = Teacher
        fields = ['id', 'nome', 'email', 'password', 'password_confirmation', 'descricao', 'idade', 'valor_hora', 'materias', 'materias_objetos', 'foto']

    def validate(self, data):
        email = data.get('user', {}).get('email', None)
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        description = data.get('description')
        hourly_price = data.get('hourly_price')
        age = data.get('age')
        name = data.get('name')
        subjects = data.get('subjects')
        errors = defaultdict(list)
        request_method = self.context.get('request_method')
        pattern = r'^[a-zA-ZÀ-ÖØ-öø-ÿ]+$'
        
        if request_method == 'PUT':
            if self.instance:
                if email is None:
                    email = None
                if not password:
                    password = None
                if not password_confirmation:
                    password_confirmation = None
                if not description:
                    description = self.instance.description
                if not hourly_price:
                    hourly_price = self.instance.hourly_price
                if not age:
                    age = self.instance.age
                if not name:
                    name = self.instance.name
                if not subjects:
                    subjects = list(self.instance.subjects.values_list('id', flat=True))            
        
        # Verificar senhas
        if (password is None or password_confirmation is None) and request_method == 'POST':
            errors['password'].append('O campo password é obrigatório')
            errors['password_confirmation'].append('O campo password_confirmation é obrigatório')
        if password is not None:
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

        # Validação de descrição
        if description is None and request_method == 'POST':
            errors['descricao'].append('A descrição é obrigatória.')
        
        if request_method == 'POST':
            if description.isnumeric():
                errors['descricao'].append('A descrição não pode ser apenas números.')
        
        # validação de valor por hora
        if hourly_price is None and request_method == 'POST':
            errors['valor_hora'].append('O valor por hora é obrigatório.')
        if hourly_price is not None:
            if hourly_price < 10:
                errors['valor_hora'].append('O valor por hora deve ser maior que 10.')
            if hourly_price > 500:
                errors['valor_hora'].append('O valor por hora deve ser menor ou igual a 500.')

        # Validação de idade
        if age is None and request_method == 'POST':
            errors['idade'].append('A idade é obrigatória.')
        if age is not None:
            if age < 18:
                errors['idade'].append('A idade deve ser maior ou igual a 18.')
            if age > 100:
                errors['idade'].append('A idade deve ser menor ou igual a 100.')
        

        # Validação de nome
        if name is None and request_method == 'POST':
            errors['nome'].append('O nome é obrigatório.')
        if name is not None:
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
        
        if subjects is None and request_method == 'POST':
            errors['materias'].append(f'O campo materias é obrigatório')
        if subjects is not None:
            if not isinstance(subjects, list):
                errors['materias'].append(f'O campo materias deve ser uma lista')
            if (len(subjects) == 0 or subjects is None) and request_method == 'POST':
                errors['materias'].append(f'O campo materias é obrigatório')
            for subject in subjects:
                if subject not in Subject.objects.values_list('id', flat=True):
                    errors['materias'].append(f'A materias com id {subject} não existe')
        
        if email is None and request_method == 'POST':
            errors['email'].append('O email é obrigatório')
        if email is not None:
            if User.objects.filter(email=email).exists():
                errors['email'].append('Este email já está cadastrado')
            if not verify_email(email) and email is not None:
                errors['email'].append('Insira um email válido')

        if errors:
            raise serializers.ValidationError(errors)
        
        return data

    def create(self, validated_data):
        # Remover campos não relacionados ao modelo Teacher
        email = validated_data.pop('user', {}).pop('email', None)
        password = validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')
        subjects_data = validated_data.pop('subjects', [])  # Remover e armazenar os dados de subjects

        # Criar o usuário associado ao professor
        user_data = {'email': email, 'password': password, 'password_confirmation': password_confirmation, 'is_teacher': True}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Criar o professor associado ao usuário
        teacher = Teacher.objects.create(user=user, **validated_data)
        if subjects_data:
            teacher.subjects.set(subjects_data)
        return teacher
    
    def update(self, instance, validated_data):
        # Remover e atualizar campos não relacionados ao modelo Teacher
        email = validated_data.pop('user', {}).pop('email', instance.user.email)
        if email != instance.user.email:
            instance.user.is_active = False
        password = validated_data.pop('password', None)
        name = validated_data.pop('name', instance.name)
        description = validated_data.pop('description', instance.description)
        hourly_price = validated_data.pop('hourly_price', instance.hourly_price)
        age = validated_data.pop('age', instance.age)
        profile_image = validated_data.pop('profile_image', instance.profile_image)
        subjects_data = validated_data.pop('subjects', None)

        # Atualizar os dados do usuário associado
        instance.user.email = email
        instance.user.is_teacher = True
        if password:
            instance.user.set_password(password)
        instance.user.save()

        # Atualizar os dados do professor
        instance.name = name
        instance.description = description
        instance.hourly_price = hourly_price
        instance.age = age
        instance.profile_image = profile_image

        if subjects_data is not None:
            instance.subjects.set(subjects_data)

        instance.save()
        return instance

    def to_representation(self, instance):
        user = instance.user
        rating = Rating.objects.filter(teacher=instance).aggregate(models.Avg('rating'))['rating__avg']
        rating = round_rating(rating)

        fields = {
            'id': instance.id,
            'nome': instance.name,
            'email': user.email,
            'idade': instance.age,
            'descricao': instance.description,
            'valor_hora': instance.hourly_price,
            'foto_perfil': instance.profile_image.url if instance.profile_image else None,
            'avaliacao': rating,
            'materias': list(instance.subjects.values_list('id', flat=True)),
            'materias_objetos': SubjectSerializer(instance.subjects.all(), many=True).data,
            'create_at': instance.create_at,
            'update_at': instance.update_at
        }

        data = {key: value for key, value in fields.items()}
        return data


class TeacherProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(
        required=True, write_only=True, source='profile_image'
    )

    class Meta:
        model = Teacher
        fields = ['foto']
        