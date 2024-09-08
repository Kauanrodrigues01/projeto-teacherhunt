from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo base para os usuários, tanto professores quanto estudantes. 
    Atributos como email e nome são compartilhados por ambos.
    """
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=100)  # Nome comum a todos os usuários
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(
        Group,
        related_name="user_groups",  # Nome único para evitar conflito com grupos específicos
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_permissions",  # Nome único para evitar conflito com permissões específicas
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def is_teacher(self):
        return hasattr(self, 'teacher_profile')

    def is_student(self):
        return hasattr(self, 'student_profile')

class Subject(models.Model):
    """
    Modelo que representa uma matéria, usada no relacionamento ManyToMany com Teacher.
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.code} - {self.name}'

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida os campos antes de salvar
        return super().save(*args, **kwargs)

class Teacher(models.Model):
    """
    Perfil de professor vinculado ao usuário.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    description = models.TextField(null=True)
    hourly_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    subjects = models.ManyToManyField(Subject, related_name="teachers", blank=True)

    def __str__(self):
        return self.user.name  # Retorna o nome do usuário diretamente

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida os campos antes de salvar
        return super().save(*args, **kwargs)

class Student(models.Model):
    """
    Perfil de estudante vinculado ao usuário.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    age = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.user.name  # Retorna o nome do usuário diretamente

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida os campos antes de salvar
        return super().save(*args, **kwargs)
