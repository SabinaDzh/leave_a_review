from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from auth.serializers import ConfirmationCodeSerializer, RegisterUserSerializer


User = get_user_model()


class RegisterUserView(views.APIView):
    """Регистрация пользователя"""

    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ConfirmationCodeView(views.APIView):
    """Подтверждение регистрации и получение токена"""
    serializer_class = ConfirmationCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data['username'])
        response_dict = {'token': str(serializer.get_token(user))}
        return Response(response_dict, status=status.HTTP_200_OK)
