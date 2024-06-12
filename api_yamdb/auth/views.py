from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ConfirmationCodeSerializer, RegisterUserSerializer
from .viewsets import CreateViewSet


User = get_user_model()


class RegisterUserViewSet(CreateViewSet):
    """Регистрация пользователя"""

    queryset = User
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)


class ConfirmationCodeView(TokenObtainPairView):
    """Подтверждение регистрации и получение токена"""
    serializer_class = ConfirmationCodeSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
