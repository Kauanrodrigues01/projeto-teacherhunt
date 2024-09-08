from django.db import models
from django.utils import timezone

# class Classroom(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='classrooms') # Usando um related_name para evitar conflitos, podera acessar as classes de um aluno com student.classrooms
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrooms') # acessa usando: teacher.classrooms
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'Aula entre {self.student.name} e {self.teacher.name}'
