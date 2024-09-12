from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Teacher, Student
from datetime import timedelta
from django.utils import timezone
from datetime import datetime

class Classroom(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrooms')
    day_of_class = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    number_of_hours = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    description_about_class = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('teacher', 'student', 'start_time')
        ordering = ['start_time']

    def clean(self):
        """
        Validação personalizada para garantir que o horário de término é posterior ao horário de início,
        que o professor e o aluno não estejam em duas aulas ao mesmo tempo,
        e que a aula não seja marcada para uma data/hora passada.
        """
        now = timezone.now()

        # Verifica se a data da aula é no passado
        if self.day_of_class < now.date():
            raise ValidationError('A data da aula não pode ser no passado.')
        
        # Verifica se o horário da aula é no passado (se for no mesmo dia)
        if self.day_of_class == now.date():
            raise ValidationError('Não é possível marcar aulas no mesmo dia. A aula deve ser marcada com antecedência.')

        # Calcula o horário de término com base no número de horas
        if self.start_time and self.number_of_hours:
            datetime_start = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.start_time))
            datetime_end = datetime_start + timedelta(hours=self.number_of_hours)
        else:
            datetime_end = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.start_time))

        # Verifica conflitos de horário para o professor
        overlapping_classes_teacher = Classroom.objects.filter(
            teacher=self.teacher,
            day_of_class=self.day_of_class
        ).exclude(pk=self.pk).filter(
            models.Q(start_time__lt=datetime_end.time(), end_time__gt=self.start_time)
        )

        # Verifica conflitos de horário para o aluno
        overlapping_classes_student = Classroom.objects.filter(
            student=self.student,
            day_of_class=self.day_of_class
        ).exclude(pk=self.pk).filter(
            models.Q(start_time__lt=datetime_end.time(), end_time__gt=self.start_time)
        )

        if overlapping_classes_teacher.exists():
            raise ValidationError('O professor já tem uma aula nesse período.')

        if overlapping_classes_student.exists():
            raise ValidationError('O aluno já tem uma aula nesse período.')

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para calcular automaticamente o horário de término e o preço
        antes de salvar a instância e atualiza o status da aula.
        """
        # Converte a string da data em um objeto datetime.date, se necessário
        if isinstance(self.day_of_class, str):
            self.day_of_class = datetime.strptime(self.day_of_class, '%Y-%m-%d').date()

        # Converte a string do horário em um objeto datetime.time, se necessário
        if isinstance(self.start_time, str):
            self.start_time = datetime.strptime(self.start_time, '%H:%M').time()
        
        if self.start_time and self.number_of_hours:
            # Calcula o horário de término
            datetime_start = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.start_time))
            datetime_end = datetime_start + timedelta(hours=self.number_of_hours)
            self.end_time = datetime_end.time()

            # Calcula o preço com base no preço por hora do professor
            self.price = self.teacher.hourly_price * self.number_of_hours

        self.full_clean()
        self.set_status_automatically()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Aula entre {self.student.name} e {self.teacher.name} - {self.get_status_display()}'

    def get_duration(self):
        """
        Retorna a duração da aula em minutos.
        """
        datetime_start = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.start_time))
        datetime_end = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.end_time))
        return (datetime_end - datetime_start).total_seconds() / 60

    def is_active(self):
        """
        Verifica se a aula está em andamento no momento atual.
        """
        now = timezone.now()
        datetime_start = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.start_time))
        datetime_end = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.end_time))
        return datetime_start <= now <= datetime_end

    def set_status_automatically(self):
        """
        Define o status da aula automaticamente com base no tempo atual.
        """
        now = timezone.now()
        datetime_start = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.start_time))
        datetime_end = timezone.make_aware(timezone.datetime.combine(self.day_of_class, self.end_time))

        if datetime_start <= now <= datetime_end:
            self.status = 'in_progress'
        elif now > datetime_end:
            self.status = 'completed'
        else:
            self.status = 'scheduled'
