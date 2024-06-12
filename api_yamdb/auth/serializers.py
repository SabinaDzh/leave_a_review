import hashlib

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()
SENDER_EMAIL = 'auth@yamdb.com'


def generate_confirmation_code(user):
    """Генерация проверочного кода для пользователя"""
    code = hashlib.md5(f'{user.date_joined}{user.id}'.encode())
    return code.hexdigest()


class RegisterUserSerializer(serializers.ModelSerializer):
    """Пользователь."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        code = generate_confirmation_code(user)
        email_text = ('Код подтверждения регистрации: '
                      f'{code}.')
        send_mail('Регистрация на YAMDB', email_text, SENDER_EMAIL,
                  (user.email,), fail_silently=False)
        return user


class ConfirmationCodeSerializer(TokenObtainPairSerializer):
    """Подтверждение кода регистрации и генерация токена."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        code = generate_confirmation_code(user)
        request = self.context.get('request')
        sent_code = request.data.get('confirmation_code')
        if code != sent_code:
            raise serializers.ValidationError('Неверный проверочный код!')

        refresh = self.get_token(user)
        data['token'] = str(refresh.access_token)
        del data['username']

        return data
