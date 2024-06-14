from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .permissions import IsAdminRole
from .serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вью для работы с пользователями для админа"""

    queryset = User
    serializer_class = UserSerializer
    permission_classes = (IsAdminRole,)
