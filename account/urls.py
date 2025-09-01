from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/account/create_user", views.ListCreateUserAPIView.as_view()),
    path("/account/list_user", views.ListCreateUserAPIView.as_view()),
]
