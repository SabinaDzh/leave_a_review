from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from auth.serializers import ConfirmationCodeSerializer, RegisterUserSerializer
from users.models import User


class RegisterUserView(views.APIView):
    """Регистрация пользователя"""

    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmationCodeView(views.APIView):
    """Подтверждение регистрации и получение токена"""
    serializer_class = ConfirmationCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

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
