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