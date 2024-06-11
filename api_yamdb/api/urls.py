
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from reviews.views import (CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet)

router_v1 = DefaultRouter()
router_v1.register('reviews', ReviewViewSet)
router_v1.register('comments', CommentViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
