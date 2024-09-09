from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def verificar_email_valido(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False