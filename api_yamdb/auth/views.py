from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from auth.serializers import ConfirmationCodeSerializer, RegisterUserSerializer
from auth.viewsets import CreateViewSet
from users.models import User


class RegisterUserViewSet(CreateViewSet):
    """Регистрация пользователя"""

    queryset = User
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        if data.status_code == status.HTTP_201_CREATED:
            data.status_code = status.HTTP_200_OK
        return data


class ConfirmationCodeView(TokenObtainPairView):
    """Подтверждение регистрации и получение токена"""
    serializer_class = ConfirmationCodeSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
