from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.timezone import now

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Campos obrigatórios para o comando createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    age = models.PositiveIntegerField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    hourly_price = models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=False)
    profile_image = models.ImageField(upload_to='teachers_image/', blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    subjects = models.ManyToManyField('Subject', related_name='teachers')

    def __str__(self):
        return f'Teacher: {self.name}'

class Subject(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    profile_image = models.ImageField(upload_to='students_image/', blank=True, null=True)
    create_at = models.DateTimeField(default=now)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Student: {self.name}'

class Rating(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ratings')
    rating = models.FloatField()
    comment = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Rating: {self.rating}'
    
    
class FavoriteTeacher(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='favorite_teachers')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='favorite_students')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Favorite Teacher: {self.teacher.name}'