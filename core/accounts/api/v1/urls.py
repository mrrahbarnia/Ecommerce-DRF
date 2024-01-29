"""
URL's for Accounts API's.
"""
from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path(
        'registration/',
        views.RegistrationApiView.as_view(),
        name='registration'
    ),
    path(
        'verification/',
        views.VerificationApiView.as_view(),
        name='verification'
    ),
    path(
        'resend/verification/',
        views.ResendVerificationApiView.as_view(),
        name='resend-verification'
    ),
    path(
        'change-password/',
        views.ChangePasswordApiView.as_view(),
        name='change-password'
    ),
    path(
        'reset-password/',
        views.ResetPasswordApiView.as_view(),
        name='reset-password'
    ),
    path('login/', views.LoginApiView.as_view(), name='login'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
