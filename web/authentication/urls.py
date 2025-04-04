from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView as LoginView,
    TokenRefreshView as LoginRefreshView,
    TokenBlacklistView as LogoutView,
)

from .views import SignUpView, LogoutAllView


app_name = "authentication"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("login-refresh/", LoginRefreshView.as_view(), name="login-refresh"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout-all/", LogoutAllView.as_view(), name="logout-all"),
]
