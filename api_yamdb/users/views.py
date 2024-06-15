from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(permission_classes=[permissions.IsAuthenticated], detail=False,
            methods=['GET', 'PATCH'])
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if 'role' in request.data and user.role != request.data['role']:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data='Нельзя изменить роль пользователя!')

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
