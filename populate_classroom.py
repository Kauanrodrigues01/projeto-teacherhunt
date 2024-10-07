import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from accounts.models import Teacher, Student
from classroom.models import Classroom

def populate_classrooms():
    classrooms_data = [
        {
            "student": random.choice(Student.objects.values_list('id', flat=True)),
            "teacher": random.choice(Teacher.objects.values_list('id', flat=True)),
            "day_of_class": datetime.now().date() + timedelta(days=i),
            "start_time": datetime.now().time().replace(hour=random.randint(8, 17), minute=0, second=0),
            "number_of_hours": random.randint(1, 3),
            "status": random.choice(['A', 'C', 'P']),
            "description_about_class": f"Descrição da aula {i}"
        } for i in range(2, 60)
    ]

    for data in classrooms_data:
        student = Student.objects.get(id=data["student"])
        teacher = Teacher.objects.get(id=data["teacher"])
        end_time = data["start_time"].replace(hour=data["start_time"].hour + data["number_of_hours"])
        price = teacher.hourly_price * data["number_of_hours"]
        Classroom.objects.create(
            student=student,
            teacher=teacher,
            day_of_class=data["day_of_class"],
            start_time=data["start_time"],
            number_of_hours=data["number_of_hours"],
            status=data["status"],
            description_about_class=data["description_about_class"],
            end_time=end_time,
            price=price
        )
        

if __name__ == "__main__":
    populate_classrooms()
