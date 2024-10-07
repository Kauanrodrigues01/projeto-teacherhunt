import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from accounts.models import User, Student

def populate_users_and_students():
    users_data = [
        {
            "email": f"Student{i}@example.com",
            "is_teacher": False,
            "is_student": True,
            "is_active": True,
            "is_staff": False,
            "name": f"Aluno {chr(65 + i)}", 
            "profile_image": None
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
        
        student = Student.objects.create(
            user=user,
            name=user_data["name"],
            profile_image=user_data["profile_image"]
        )
        print(f'Usuário e aluno criados: {user.email} - {student.name}')

if __name__ == "__main__":
    populate_users_and_students()
