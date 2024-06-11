from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()
router_v1.register('reviews', ReviewViewSet)
router_v1.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
