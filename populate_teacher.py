import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from accounts.models import User, Teacher, Subject

def populate_users_and_teachers():
    users_data = [
        {
            "email": f"teacher{i}@example.com",
            "is_teacher": True,
            "is_student": False,
            "is_active": True,
            "is_staff": False,
            "name": f"Professor {chr(65 + i)}", 
            "age": random.randint(30, 50),
            "description": f"Professor de disciplina {i}",
            "hourly_price": round(random.uniform(40.00, 100.00), 2),
            "profile_image": None,
            "subjects": [random.choice(Subject.objects.values_list('id', flat=True)) for _ in range(random.randint(1, 6))]
        }
        for i in range(0, 20)  
    ]

    for user_data in users_data:
        user = User.objects.create_user(
            email=user_data["email"],
            password='@Password123',
            is_teacher=user_data["is_teacher"],
            is_student=user_data["is_student"],
            is_active=user_data["is_active"],
            is_staff=user_data["is_staff"]
        )
        
        teacher = Teacher.objects.create(
            user=user,
            name=user_data["name"],
            age=user_data["age"],
            description=user_data["description"],
            hourly_price=user_data["hourly_price"],
            profile_image=user_data["profile_image"]
        )
        teacher.subjects.set(Subject.objects.filter(id__in=user_data["subjects"]))
        print(f'Usuário e professor criados: {user.email} - {teacher.name}')

if __name__ == "__main__":
    populate_users_and_teachers()
