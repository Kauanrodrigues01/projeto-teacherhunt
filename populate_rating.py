import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from accounts.models import Student, Teacher, Rating

def populate_ratings():
    data =[
        {
            "student": random.choice(Student.objects.values_list('id', flat=True)),
            "teacher": random.choice(Teacher.objects.values_list('id', flat=True)),
            "rating": round(random.uniform(0, 5.0) * 2) / 2,
            "comment": f"Comentário Aleatório {i}"
        } for i in range(0, 60)
    ]
    
    for value in data:
        student = Student.objects.get(id=value["student"])
        teacher = Teacher.objects.get(id=value["teacher"])
        Rating.objects.create(
            student=student,
            teacher=teacher,
            rating=value["rating"],
            comment=value["comment"]
        )

if __name__ == "__main__":
    populate_ratings()
