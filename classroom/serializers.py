from rest_framework import serializers
from .models import Classroom

class ClassroomSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'student', 'teacher', 'student_name', 'teacher_name', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def validate(self, data):
        student = data.get('student')
        teacher = data.get('teacher')

        # Validação para garantir que a mesma combinação de aluno e professor não exista
        if Classroom.objects.filter(student=student, teacher=teacher).exists():
            raise serializers.ValidationError('Já existe uma aula agendada entre este aluno e este professor.')

        return data