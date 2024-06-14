from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from reviews.views import (
    # CategoryViewSet, GenreViewSet,
    TitleViewSet,
    ReviewViewSet, CommentViewSet)

from users.views import UserViewSet


router_v1 = DefaultRouter()
router_v1.register('reviews', ReviewViewSet)
router_v1.register('comments', CommentViewSet)
# router_v1.register('categories', CategoryViewSet, basename='categories')
# router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('auth.urls')),
]
