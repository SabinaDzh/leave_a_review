from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS)
from rest_framework.response import Response

from api.filters import TitleViewSetFilter
from api.mixins import (CreateListDestroyViewSet,
                        GetPostPatchDeleteViewSet)
from api.permissions import (IsAdminOrReadOnly, IsAdminRole,
                             IsAuthorAdminModeratorOrReadOnly)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    UserSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategoryViewSet(CreateListDestroyViewSet):
    """Viewset для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Viewset для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(GetPostPatchDeleteViewSet):
    """Viewset для произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    serializer_class = TitleReadSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleViewSetFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(GetPostPatchDeleteViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs['title_id']
        return context

    def perform_create(self, serializer):
        current_title = self.get_title()
        serializer.save(author=self.request.user, title=current_title)


class CommentViewSet(GetPostPatchDeleteViewSet):

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'],
                                 title_id=self.kwargs['title_id'])

    def get_queryset(self):
        review = self.get_review()
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        current_review = self.get_review()
        serializer.save(author=self.request.user, review=current_review)


class UserViewSet(GetPostPatchDeleteViewSet):
    """Вью для работы с пользователями для админа"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    filter_backends = (filters.SearchFilter,)

    permission_classes = (IsAdminRole,)
    search_fields = ('username',)

    @action(permission_classes=[permissions.IsAuthenticated], detail=False,
            methods=['GET', 'PATCH'])
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
