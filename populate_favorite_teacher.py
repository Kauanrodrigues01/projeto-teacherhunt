import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from accounts.models import Student, Teacher, FavoriteTeacher

def populate_favorite_teachers():
    data =[
        {
            "student": random.choice(Student.objects.values_list('id', flat=True)),
            "teacher": random.choice(Teacher.objects.values_list('id', flat=True))
        } for i in range(0, 20)
    ]

    for value in data:
        student = Student.objects.get(id=value["student"])
        teacher = Teacher.objects.get(id=value["teacher"])
        FavoriteTeacher.objects.create(
            student=student,
            teacher=teacher
        )
        print(f'Professor favorito adicionado: {teacher.name} - {student.name}')

if __name__ == "__main__":
    populate_favorite_teachers()
