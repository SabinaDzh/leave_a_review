from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework import viewsets

from .pagination import UsersPagination
from .permissions import IsAdminRole
from .serializers import UserSerializer
from .viewsets import GetPostPatchDeleteViewSet


User = get_user_model()


class UserViewSet(GetPostPatchDeleteViewSet):
    """Вью для работы с пользователями для админа"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    filter_backends = (filters.SearchFilter,)

    pagination_class = UsersPagination
    permission_classes = (IsAdminRole,)
    search_fields = ('username',)
