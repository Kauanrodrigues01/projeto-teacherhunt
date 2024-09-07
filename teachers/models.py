from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import TeacherManager


class Subject(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.code} - {self.name}'
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Teacher(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)
    age = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)
    hourly_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="teachers", blank=True, default='')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = TeacherManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
