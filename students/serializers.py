import django.utils.timezone
from rest_framework import serializers
from .models import Student
from django.utils import timezone

class StudentSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source='name', required=True, min_length=3, max_length=100)
    data_aula = serializers.DateTimeField(source='class_date', required=True)
    class Meta:
        model = Student
        fields = ['id', 'nome', 'email', 'data_aula', 'created_at', 'updated_at']
        extra_kwargs = {
            'email': {'required': True, 'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
        
    def validate_data_aula(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('A data da aula deve ser no futuro')
        if value in Student.objects.values_list('class_date', flat=True):
            raise serializers.ValidationError('Já existe um aluno com a mesma data de aula')
        return value