from rest_framework import mixins, viewsets, filters

from api.permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Миксин для Category/Genre ViewSet."""
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    """Разрешенные методы: GET, POST, PATCH, DELETE"""
    http_method_names = ['get', 'post', 'patch', 'delete']
