from django.urls import path

from auth.views import ConfirmationCodeView, RegisterUserView


urlpatterns = [
    path('signup/', RegisterUserView.as_view(), name='signup'),
    path('token/', ConfirmationCodeView.as_view(), name='token_obtain'),
]
