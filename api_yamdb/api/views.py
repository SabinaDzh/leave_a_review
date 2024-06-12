from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (SAFE_METHODS)

from reviews.models import Category, Genre, Title
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from api.permissions import IsAdminOrReadOnly
from api.mixins import CreateListDestroyViewSet



class UsersViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """Viewset для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Viewset для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset для произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer
