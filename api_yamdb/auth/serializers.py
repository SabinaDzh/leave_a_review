from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth.functions import generate_confirmation_code, send_confirmation_code
from users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """Пользователь."""

    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z')
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user = User.objects.filter(username=validated_data['username']).first()
        if not user:
            user = User.objects.create(**validated_data)
        send_confirmation_code(user)
        return user

    def validate(self, data):
        user_same_email = User.objects.filter(email=data['email']).first()
        user_same_username = User.objects.filter(
            username=data['username']).first()
        if (
            user_same_username
            and user_same_username.email != data['email']
        ):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!')
        if (
            user_same_email
            and user_same_email.username != data['username']
        ):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует!'
            )
        return super().validate(data)

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'Нельзя указать "me" в поле username!'
            )
        return data


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
