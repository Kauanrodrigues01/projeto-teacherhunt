from rest_framework import serializers
from accounts.models import Student
from accounts.serializers import UserSerializer
from accounts.models import Subject

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True, required=False)

    class Meta:
        model = Student
        fields = ['user', 'subjects']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_student'] = True
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student = Student.objects.create(user=user)
        if 'subjects' in validated_data:
            student.subjects.set(validated_data['subjects'])
        return student

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