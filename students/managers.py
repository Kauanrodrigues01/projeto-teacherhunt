from django.contrib.auth.models import BaseUserManager

class StudentManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """
        Cria e retorna um usuário do tipo Student com um email e senha fornecidos.
        """
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Cria e retorna um superusuário do tipo Student com um email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuários devem ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuários devem ter is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)
