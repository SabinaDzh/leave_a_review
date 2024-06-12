from rest_framework import mixins
from rest_framework import viewsets


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Cоздание объекта"""
    pass
