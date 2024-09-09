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
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    subjects_obejcts = SubjectSerializer(many=True, source="subjects", read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'age', 'description', 'hourly_price', 'profile_image', 'password', 'password_confirmation', 'name', 'email', 'subjects', 'subjects_obejcts']

    def validate(self, data):
        """Verificar se os campos são válidos."""
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        description = data.get('description')
        hourly_price = data.get('hourly_price')
        age = data.get('age')
        name = data.get('name')
        errors = defaultdict(list)

        # Verificar senhas
        if password != password_confirmation:
            errors["password"].append("As senhas não coincidem.")

        # Validação de descrição
        if not description or description.isnumeric():
            errors["description"].append("A descrição não pode ser vazia e não pode ser apenas números.")

        # Validação de preço por hora
        if hourly_price is None or hourly_price <= 0:
            errors["hourly_price"].append("O preço por hora deve ser maior que zero.")
        elif hourly_price > 500:
            errors["hourly_price"].append("O preço por hora deve ser menor ou igual a 500.")

        # Validação de idade
        if age is None or age <= 0:
            errors["age"].append("A idade deve ser maior que zero.")
        elif age > 120:
            errors["age"].append("A idade deve ser menor ou igual a 120.")

        # Validação de nome
        if not name or name.isnumeric():
            errors["name"].append("O nome não pode ser vazio e não pode ser apenas números.")
        elif len(name) < 3:
            errors["name"].append("O nome deve ter no mínimo 3 caracteres.")
        elif len(name) > 255:
            errors["name"].append("O nome deve ter no máximo 255 caracteres.")

        if errors:
            raise serializers.ValidationError(errors)
        
        return data

    def create(self, validated_data):
        # Remover campos não relacionados ao modelo Teacher
        name = validated_data.pop('name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')
        subjects_data = validated_data.pop('subjects', [])  # Remover e armazenar os dados de subjects

        # Criar o usuário associado ao professor
        user_data = {"name": name, "email": email, "password": password, "password_confirmation": password_confirmation}
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
        name = validated_data.pop('name', instance.user.name)
        email = validated_data.pop('email', instance.user.email)
        password = validated_data.pop('password', None)
        description = validated_data.pop('description', instance.description)
        hourly_price = validated_data.pop('hourly_price', instance.hourly_price)
        age = validated_data.pop('age', instance.age)
        profile_image = validated_data.pop('profile_image', instance.profile_image)
        subjects_data = validated_data.pop('subjects', None)

        # Atualizar os dados do usuário associado
        instance.user.name = name
        instance.user.email = email
        if password:
            instance.user.set_password(password)
        instance.user.save()

        # Atualizar os dados do professor
        instance.description = description
        instance.hourly_price = hourly_price
        instance.age = age
        instance.profile_image = profile_image

        if subjects_data is not None:
            # Atualizar os assuntos do professor
            instance.subjects.set(subjects_data)

        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Personalizar a saída de dados."""
        # Transformar o objeto 'instance' em um dicionário
        data = super().to_representation(instance)

        # Supondo que 'user' seja uma relação no modelo 'instance'
        user = instance.user
        age = data.pop("age")
        description = data.pop("description")
        hourly_price = data.pop("hourly_price")
        profile_image = data.pop("profile_image")
        subjects = data.pop("subjects", [])
        subjects_obejcts = data.pop("subjects_obejcts", [])
        
        data["email"] = user.email
        data["name"] = user.name
        data["age"] = age
        data["description"] = description
        data["hourly_price"] = hourly_price
        data["profile_image"] = profile_image
        data["subjects"] = subjects
        data["subjects_obejcts"] = subjects_obejcts
        return data

class TeacherProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(
        required=True, write_only=True, source="profile_image"
    )

    class Meta:
        model = Teacher
        fields = ("foto",)
        