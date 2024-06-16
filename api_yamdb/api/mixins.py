from rest_framework import mixins, viewsets
from rest_framework.response import Response


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    """Разрешенные методы: GET, POST, PATCH, DELETE"""
    http_method_names = ['get', 'post', 'patch', 'delete']
