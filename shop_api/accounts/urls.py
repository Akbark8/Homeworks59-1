from django.urls import path
from .views import AuthorizationAPIView, RegistrationAPIView, ConfirmUserAPIView
from .views import (
    AuthorizationAPIView,
    RegistrationAPIView,
    ConfirmUserAPIView,
    GoogleAuthorizationAPIView,
)

urlpatterns = [
    path('login/', AuthorizationAPIView.as_view()),
    path('login/google/', GoogleAuthorizationAPIView.as_view()),
    path('register/', RegistrationAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),
]