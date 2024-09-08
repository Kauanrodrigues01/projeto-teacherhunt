from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from accounts.serializers import UserSerializer
from accounts.models import Teacher, Subject

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
    user = UserSerializer()  # Aninha o UserSerializer para criar o usuário junto
    descricao = serializers.CharField(source='description', required=True, write_only=True)
    valor_hora = serializers.DecimalField(max_digits=5, decimal_places=2, source='hourly_price', required=True, write_only=True)
    foto = serializers.ImageField(source='profile_image', required=False, write_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'descricao', 'valor_hora', 'foto', 'subjects']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.subjects.set(self.initial_data.get('subjects'))
        return teacher

    def update(self, instance, validated_data):
        subjects = validated_data.pop('subjects', None)
        instance.description = validated_data.get('description', instance.description)
        instance.hourly_price = validated_data.get('hourly_price', instance.hourly_price)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)

        if subjects:
            instance.subjects.set(subjects)

        instance.save()

        user_data = validated_data.get('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        return instance

class TeacherProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(
        required=True, write_only=True, source="profile_image"
    )

    class Meta:
        model = Teacher
        fields = ("foto",)
        