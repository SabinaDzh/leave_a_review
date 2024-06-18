from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from auth.functions import generate_confirmation_code, send_confirmation_code
from users.models import User


class RegisterUserSerializer(serializers.Serializer):
    """Пользователь."""

    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(
        max_length=254,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data['username'], defaults=validated_data)
        send_confirmation_code(user)
        return user

    def validate(self, data):

        user_same_email = User.objects.filter(email=data['email']).first()
        user_same_username = User.objects.filter(
            username=data['username']).first()

        if user_same_email != user_same_username:

            message_template = (
                'Пользователь с таким {field_name} уже существует!')

            error_messages_dict = {
                key: value for key, value in zip(
                    ['username', 'email'],
                    [user_same_username, user_same_email])
            }

            error_messages = [
                message_template.format(field_name=key)
                for key, value in error_messages_dict.items() if value]

            raise serializers.ValidationError(error_messages)

        return super().validate(data)

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'Нельзя указать "me" в поле username!'
            )
        return data


class ConfirmationCodeSerializer(TokenObtainSerializer):
    """Подтверждение кода регистрации и генерация токена."""

    token_class = AccessToken
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        code = generate_confirmation_code(user)
        if code != data['confirmation_code']:
            raise serializers.ValidationError('Неверный проверочный код!')

        return data
