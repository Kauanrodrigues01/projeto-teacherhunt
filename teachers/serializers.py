from rest_framework import serializers
from accounts.models import Teacher, Subject
from accounts.serializers import UserSerializer
from collections import defaultdict

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name")
        
    def validate(self, attrs):
        name = attrs.get('name')
        
        if not name or name.isdigit():
            raise serializers.ValidationError({"name": "O nome deve ser um texto válido e não pode ser apenas números."})

        return super().validate(attrs)
        

class TeacherSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True, source="name")
    email = serializers.EmailField(required=True, source='user.email')
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    descricao = serializers.CharField(required=True, source="description")
    idade = serializers.IntegerField(required=True, source="age")
    valor_hora = serializers.DecimalField(required=True, source="hourly_price", max_digits=6, decimal_places=2)
    materias = serializers.ListField(child=serializers.IntegerField(), required=True, source="subjects")
    materias_objetos = SubjectSerializer(many=True, source="subjects", read_only=True)
    foto = serializers.ImageField(required=False, source="profile_image")

    class Meta:
        model = Teacher
        fields = ['id', 'nome', 'email', 'password', 'password_confirmation', 'descricao', 'idade', 'valor_hora', 'materias', 'materias_objetos', 'foto']

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        description = data.get('description')
        hourly_price = data.get('hourly_price')
        age = data.get('age')
        name = data.get('name')
        materias = data.get('subjects')
        errors = defaultdict(list)

        # Verificar senhas
        if password != password_confirmation:
            errors["password"].append("As senhas não coincidem.")

        # Validação de descrição
        if not description or description.isnumeric():
            errors["descricao"].append("A descrição não pode ser vazia e não pode ser apenas números.")

        # Validação de preço por hora
        if hourly_price is None or hourly_price <= 0:
            errors["valor_hora"].append("O valor por hora deve ser maior que zero.")
        elif hourly_price > 500:
            errors["valor_hora"].append("O valor por hora deve ser menor ou igual a 500.")

        # Validação de idade
        if age is None or age <= 0:
            errors["idade"].append("A idade deve ser maior que zero.")
        elif age > 120:
            errors["idade"].append("A idade deve ser menor ou igual a 120.")

        # Validação de nome
        if not name or name.isnumeric():
            errors["nome"].append("O nome não pode ser vazio e não pode ser apenas números.")
        elif len(name) < 3:
            errors["nome"].append("O nome deve ter no mínimo 3 caracteres.")
        elif len(name) > 255:
            errors["nome"].append("O nome deve ter no máximo 255 caracteres.")

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
        user_data = {"email": email, "password": password, "password_confirmation": password_confirmation, "is_teacher": True}
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
        """Personalizar a saída de dados."""
        data = {}
        user = instance.user
        
        id = instance.id
        age = instance.age
        name = instance.name
        description = instance.description
        hourly_price = instance.hourly_price
        profile_image = instance.profile_image.url if instance.profile_image else None
        subjects = list(instance.subjects.values_list('id', flat=True))
        subjects_obejcts = SubjectSerializer(instance.subjects.all(), many=True).data
        
        data["id"] = id
        data["email"] = user.email
        data["nome"] = name
        data["idade"] = age
        data["descricao"] = description
        data["valor_hora"] = hourly_price
        data["foto"] = profile_image
        data["materias"] = subjects
        data["materias_objetos"] = subjects_obejcts
        return data


class TeacherProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(
        required=True, write_only=True, source="profile_image"
    )

    class Meta:
        model = Teacher
        fields = ("foto",)
        