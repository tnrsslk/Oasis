from django.core.mail import send_mail
from django.conf import settings

def send_forget_password_email(email, token):
    subject = 'Reset Password'
    message = f'Hi, click on link to reset your password http://127.0.0.1:8000/reset_password/{token}/'
     # Адрес отправителя
    email_from = settings.EMAIL_HOST_USER
    # Список получателей (в данном случае, один адрес электронной почты)
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True