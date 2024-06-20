import hashlib

from django.core.mail import send_mail

from django.conf import settings


def generate_confirmation_code(user):
    """Генерация проверочного кода для пользователя"""
    code = hashlib.md5(f'{user.date_joined}{user.id}'.encode())
    return code.hexdigest()


def send_confirmation_code(user):
    """Отправка кода подтверждения"""
    code = generate_confirmation_code(user)
    email_text = (f'Код подтверждения регистрации: {code}.')
    send_mail('Регистрация на YAMDB', email_text, settings.SENDER_EMAIL,
              (user.email,), fail_silently=False)
