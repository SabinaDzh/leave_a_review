from django.urls import include, path
from rest_framework import routers

from api.views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, ReviewViewSet, CommentViewSet,
    UserViewSet)


router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'titles\/(?P<title_id>.+?)\/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles\/(?P<title_id>.+?)\/reviews\/(?P<review_id>.+?)/comments',
    CommentViewSet, basename='comments')
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('auth.urls')),
]
