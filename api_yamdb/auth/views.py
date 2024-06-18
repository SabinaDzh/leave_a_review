from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

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


class ConfirmationCodeView(views.APIView):
    """Подтверждение регистрации и получение токена"""
    serializer_class = ConfirmationCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request: views.Request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(
                username=serializer.validated_data['username'])
            serializer.validated_data['token'] = (
                str(serializer.get_token(user)))
            del serializer.validated_data['username']
            del serializer.validated_data['confirmation_code']
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)

        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)
