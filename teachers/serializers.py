from rest_framework import serializers
from accounts.models import Teacher, Subject
from accounts.serializers import UserSerializer

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
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'age', 'description', 'hourly_price', 'profile_image']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_teacher'] = True
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

class TeacherProfileImageSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(
        required=True, write_only=True, source="profile_image"
    )

    class Meta:
        model = Teacher
        fields = ("foto",)
        