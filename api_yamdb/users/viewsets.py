from rest_framework import viewsets


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    """Разрешенные методы: GET, POST, PATCH, DELETE"""
    http_method_names = ['get', 'post', 'patch', 'delete']
