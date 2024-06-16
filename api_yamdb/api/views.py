from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS)
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from api.permissions import (IsAdminOrReadOnly, IsAdminRole,
                             IsAuthorAdminModeratorOrReadOnly)
from api.filters import TitleViewSetFilter
from api.mixins import (CreateListDestroyViewSet,
                        GetPostPatchDeleteViewSet)
from reviews.serializers import ReviewSerializer, CommentSerializer
from users.serializers import UserSerializer
from .pagination import Pagination


User = get_user_model()


class CategoryViewSet(CreateListDestroyViewSet):
    """Viewset для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    """Viewset для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(GetPostPatchDeleteViewSet):
    """Viewset для произведений."""
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitleReadSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleViewSetFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(GetPostPatchDeleteViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
    pagination_class = Pagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        current_title = self.get_title()
        serializer.save(author=self.request.user, title=current_title)

    def partial_update(self, request, *args, **kwargs):
        instance = Review.objects.get(pk=kwargs['pk'])
        serializer = self.serializer_class(instance, data=request.data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentViewSet(GetPostPatchDeleteViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(GetPostPatchDeleteViewSet):
    """Вью для работы с пользователями для админа"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    filter_backends = (filters.SearchFilter,)

    pagination_class = Pagination
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
