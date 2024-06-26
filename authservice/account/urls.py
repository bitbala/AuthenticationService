from django.urls import path
from .views import IsAuthenticatedView, RegisterView, ChangePasswordView, ForgotPasswordView, PasswordResetView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/is_authenticated/', IsAuthenticatedView.as_view(), name="is_authenticated"),
    path('api/change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('api/forgot_password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('api/password_reset/', PasswordResetView.as_view(), name="password_reset"),
]