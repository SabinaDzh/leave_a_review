from django.urls import include, path
from rest_framework import routers

from auth.views import ConfirmationCodeView, RegisterUserViewSet


router = routers.DefaultRouter()
router.register('signup', RegisterUserViewSet, 'signup')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', ConfirmationCodeView.as_view(), name='token_obtain'),
]
