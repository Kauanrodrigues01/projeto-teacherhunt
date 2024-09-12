import re
from rest_framework import serializers
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import Classroom
from accounts.models import User, Student, Teacher

class ClassroomSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), required=True)
    nome_estudante = serializers.CharField(source='student.name', read_only=True)
    nome_professor = serializers.CharField(source='teacher.name', read_only=True)
    dia_da_aula = serializers.DateField(source='day_of_class', format='%d/%m/%Y', required=True)
    horario_de_inicio = serializers.TimeField(source='start_time', required=True)
    horario_de_termino = serializers.TimeField(source='end_time', read_only=True)
    numero_de_horas = serializers.IntegerField(source='number_of_hours', required=True)
    preco = serializers.DecimalField(source='price', max_digits=6, decimal_places=2, read_only=True)
    status = serializers.ChoiceField(choices=Classroom.STATUS_CHOICES, read_only=True)
    descricao_aula = serializers.CharField(source='description_about_class', required=False)
    
    class Meta:
        model = Classroom
        fields = ['id', 'student', 'teacher', 'nome_estudante', 'nome_professor', 'dia_da_aula', 'horario_de_inicio', 'horario_de_termino', 'numero_de_horas', 'preco', 'status', 'descricao_aula']
        
    def validate(self, data):
        """
        Validação personalizada para garantir que o horário de término é posterior ao horário de início,
        que o professor e o aluno não estejam em duas aulas ao mesmo tempo,
        e que a aula não seja marcada para uma data/hora passada.
        """
        now = timezone.now()
        classroom_id = self.instance.pk if self.instance else None

        # Verifica se a data da aula é no passado
        if data['day_of_class'] < now.date():
            raise serializers.ValidationError('A data da aula não pode ser no passado.')

        # Verifica se o horário da aula é no passado (se for no mesmo dia)
        if data['day_of_class'] == now.date():
            raise serializers.ValidationError('Não é possível marcar aulas no mesmo dia. A aula deve ser marcada com antecedência.')

        # Calcula o horário de término com base no número de horas
        if data['start_time'] and data['number_of_hours']:
            datetime_start = timezone.make_aware(timezone.datetime.combine(data['day_of_class'], data['start_time']))
            datetime_end = datetime_start + timedelta(hours=data['number_of_hours'])
        else:
            datetime_end = timezone.make_aware(timezone.datetime.combine(data['day_of_class'], data['start_time']))

        # Verifica conflitos de horário para o professor
        overlapping_classes_teacher = Classroom.objects.filter(
            teacher=data['teacher'],
            day_of_class=data['day_of_class']
        ).exclude(pk=classroom_id).filter(
            models.Q(start_time__lt=datetime_end.time(), end_time__gt=data['start_time'])
        )

        # Verifica conflitos de horário para o aluno
        overlapping_classes_student = Classroom.objects.filter(
            student=data['student'],
            day_of_class=data['day_of_class']
        ).exclude(pk=classroom_id).filter(
            models.Q(start_time__lt=datetime_end.time(), end_time__gt=data['start_time'])
        )

        if overlapping_classes_teacher.exists():
            raise serializers.ValidationError('O professor já tem uma aula marcada nesse horário.')

        if overlapping_classes_student.exists():
            raise serializers.ValidationError('O estudante já tem uma aula marcada nesse horário.')

        return data
    
    def create(self, validated_data):
        classroom = Classroom.objects.create(
            student=validated_data['student'],
            teacher=validated_data['teacher'],
            day_of_class=validated_data['day_of_class'],
            start_time=validated_data['start_time'],
            number_of_hours=validated_data['number_of_hours'],
            description_about_class=validated_data.get('description_about_class', None)
        )
        classroom.save()
        return classroom
    
    def update(self, instance, validated_data):
        student = validated_data.get('student', instance.student)
        teacher = validated_data.get('teacher', instance.teacher)
        day_of_class = validated_data.get('day_of_class', instance.day_of_class)
        start_time = validated_data.get('start_time', instance.start_time)
        number_of_hours = validated_data.get('number_of_hours', instance.number_of_hours)
        description_about_class = validated_data.get('description_about_class', instance.description_about_class)
        instance.student = student
        instance.teacher = teacher
        instance.day_of_class = day_of_class
        instance.start_time = start_time
        instance.number_of_hours = number_of_hours
        instance.description_about_class = description_about_class
        instance.save()
        return super().update(instance, validated_data)