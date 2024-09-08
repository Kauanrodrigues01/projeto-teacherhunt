from rest_framework import serializers
from accounts.models import Student
from accounts.serializers import UserSerializer

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Aninha o UserSerializer para criar o usuário junto

    class Meta:
        model = Student
        fields = ['id', 'user', 'age']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        instance.age = validated_data.get('age', instance.age)
        instance.save()

        user_data = validated_data.get('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

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