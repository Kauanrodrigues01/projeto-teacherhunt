from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import EmailMessage

def verify_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def send_email(subject, message, to_email):
    '''
    # The subject is the subject of the email.
    # The message is the body of the email.
    # The to_email is the email address to send the email to.
    '''
    email = EmailMessage(
        subject=subject,
        body=message,
        to=[to_email]
    )
    email.send()
    
    
def round_rating(avaliacao):
    if avaliacao is None:
        return None
    valor = avaliacao * 2
    if valor - int(valor) == 0.5:
        valor += 0.1
    valor_arredondado = round(valor)
    
    if valor % 1 == 0.25:
        valor_arredondado += 1
    elif valor % 1 == 0.75:
        valor_arredondado += 1 

    return valor_arredondado / 2
