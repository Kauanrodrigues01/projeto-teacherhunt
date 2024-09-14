import re
from rest_framework import serializers
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import Classroom
from accounts.models import User, Student, Teacher
from datetime import datetime, date
from collections import defaultdict

class ClassroomSerializer(serializers.ModelSerializer):
    aluno = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student')
    professor = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), source='teacher')
    nome_estudante = serializers.CharField(source='student.name', read_only=True)
    nome_professor = serializers.CharField(source='teacher.name', read_only=True)
    dia_da_aula = serializers.DateField(source='day_of_class', format='%d/%m/%Y',  required=False)
    horario_de_inicio = serializers.TimeField(source='start_time', required=False)
    horario_de_termino = serializers.TimeField(source='end_time', read_only=True)
    numero_de_horas = serializers.IntegerField(source='number_of_hours',  required=False)
    preco = serializers.DecimalField(source='price', max_digits=6, decimal_places=2, read_only=True)
    status = serializers.SerializerMethodField()
    descricao_aula = serializers.CharField(source='description_about_class', required=False)
    
    class Meta:
        model = Classroom
        fields = ['id', 'aluno', 'professor', 'nome_estudante', 'nome_professor', 'dia_da_aula', 'horario_de_inicio', 'horario_de_termino', 'numero_de_horas', 'preco', 'status', 'descricao_aula']

    def get_status(self, obj):
        return obj.get_status_display()

    def validate(self, data):
        now = timezone.now()
        classroom_id = self.instance.pk if self.instance else None
        day_of_class = data.get('day_of_class', None)
        start_time = data.get('start_time', None)
        number_of_hours = data.get('number_of_hours', None)
        teacher = data.get('teacher', None)
        student = data.get('student')
        # Gera uma lista de horários válidos de 07:00 até 20:00 com um intervalo de uma hora
        horarios_validos = [f"{hour:02d}:00" for hour in range(7, 21)]

        errors = defaultdict(list)
        day_of_class_date_obj = datetime.strptime(day_of_class, '%Y-%m-%d').date() if not isinstance(day_of_class, date) else day_of_class

        if self.context.get('request_method') == 'PUT':
            if self.instance.day_of_class - now.date() < timedelta(days=2) and day_of_class_date_obj - now.date() < timedelta(days=2):
                raise serializers.ValidationError('Não é possível alterar aulas com menos de 2 dias de antecedência.')
            if day_of_class is None:
                day_of_class = self.instance.day_of_class
            if start_time is None:
                start_time = self.instance.start_time
            if number_of_hours is None:
                number_of_hours = self.instance.number_of_hours

        if (str(start_time)[:-3]) not in horarios_validos:
            errors['horario_de_inicio'].append('Horário inválido. Os horários permitidos são de 07:00 até 20:00 com um intervalo de uma hora.')

        if Classroom.objects.filter(day_of_class=day_of_class, start_time=start_time, teacher=teacher, student=student).exclude(pk=classroom_id).exists():
            errors['error'].append('Já existe uma aula marcada para esse dia e horário.') 

        if day_of_class == now.date():
           errors['dia_da_aula'].append('Não é possível marcar aulas no mesmo dia. A aula deve ser marcada com antecedência.')

        if day_of_class < now.date():
            errors['dia_da_aula'].append('A data da aula não pode ser no passado.')

        if number_of_hours < 1:
            errors['numero_de_horas'].append('O número de horas deve ser maior que 0.')

        if start_time and number_of_hours:
            datetime_start = timezone.make_aware(timezone.datetime.combine(day_of_class, start_time))
            datetime_end = datetime_start + timedelta(hours=number_of_hours)
        else:
            datetime_end = timezone.make_aware(timezone.datetime.combine(day_of_class, start_time))

        overlapping_classes_teacher = Classroom.objects.filter(
            teacher=teacher,
            day_of_class=day_of_class
        ).exclude(pk=classroom_id).filter(
            models.Q(start_time__lt=datetime_end.time(), end_time__gt=start_time)
        )

        overlapping_classes_student = Classroom.objects.filter(
            student=student,
            day_of_class=day_of_class
        ).exclude(pk=classroom_id).filter(
            models.Q(start_time__lt=datetime_end.time(), end_time__gt=start_time)
        )

        if overlapping_classes_teacher.exists():
            errors['professor'].append('O professor já tem uma aula marcada nesse horário.')

        if overlapping_classes_student.exists():
            errors['aluno'].append('O estudante já tem uma aula marcada nesse horário.')

        if errors:
            raise serializers.ValidationError(errors)
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