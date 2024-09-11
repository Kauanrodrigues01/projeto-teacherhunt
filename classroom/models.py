from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import Teacher, Student
from datetime import timedelta
from django.utils import timezone

class Classroom(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),  # nova_aula
        ('in_progress', 'In Progress'),  # aula_em_andamento
        ('completed', 'Completed'),  # aula_concluida
        ('cancelled', 'Cancelled'),  # cancelada
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrooms')
    day_of_class = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()  # end_time = start_time + number_of_hours
    price = models.DecimalField(max_digits=6, decimal_places=2)
    number_of_hours = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('teacher', 'student', 'start_time', 'day_of_class')  # Evita aulas duplicadas no mesmo horário
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
        if self.day_of_class == now.date() and self.start_time < now.time():
            raise ValidationError('O horário da aula não pode ser no passado.')

        # Verifica se o horário de término é posterior ao horário de início
        if self.end_time <= self.start_time:
            raise ValidationError('O horário de término deve ser posterior ao horário de início.')

        # Verifica conflitos de horário para o professor
        overlapping_classes_teacher = Classroom.objects.filter(
            teacher=self.teacher,
            day_of_class=self.day_of_class,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)

        # Verifica conflitos de horário para o aluno
        overlapping_classes_student = Classroom.objects.filter(
            student=self.student,
            day_of_class=self.day_of_class,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)

        if overlapping_classes_teacher.exists():
            raise ValidationError('O professor já tem uma aula nesse horário.')

        if overlapping_classes_student.exists():
            raise ValidationError('O aluno já tem uma aula nesse horário.')

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para calcular automaticamente o horário de término e o preço
        antes de salvar a instância e atualiza o status da aula.
        """
        if self.start_time and self.number_of_hours:
            # Calcula o horário de término
            datetime_start = timezone.datetime.combine(self.day_of_class, self.start_time)
            datetime_end = datetime_start + timedelta(hours=self.number_of_hours)
            self.end_time = datetime_end.time()

            # Calcula o preço com base no preço por hora do professor
            self.price = self.teacher.hourly_price * self.number_of_hours

        # Define o status da aula automaticamente
        self.set_status_automatically()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Aula entre {self.student.name} e {self.teacher.name} - {self.get_status_display()}'

    def get_duration(self):
        """
        Retorna a duração da aula em minutos.
        """
        datetime_start = timezone.datetime.combine(self.day_of_class, self.start_time)
        datetime_end = timezone.datetime.combine(self.day_of_class, self.end_time)
        return (datetime_end - datetime_start).total_seconds() / 60

    def is_active(self):
        """
        Verifica se a aula está em andamento no momento atual.
        """
        now = timezone.now()
        datetime_start = timezone.datetime.combine(self.day_of_class, self.start_time)
        datetime_end = timezone.datetime.combine(self.day_of_class, self.end_time)
        return datetime_start <= now <= datetime_end

    def set_status_automatically(self):
        """
        Define o status da aula automaticamente com base no tempo atual.
        """
        now = timezone.now()
        datetime_start = timezone.datetime.combine(self.day_of_class, self.start_time)
        datetime_end = timezone.datetime.combine(self.day_of_class, self.end_time)

        if datetime_start <= now <= datetime_end:
            self.status = 'in_progress'
        elif now > datetime_end:
            self.status = 'completed'
        else:
            self.status = 'scheduled'
