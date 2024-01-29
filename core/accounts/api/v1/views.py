"""
Accounts app view's.
"""
import logging

from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegistrationSerializer,
    VerificationSerializer,
    LoginSerializer
)

logger = logging.getLogger(__name__)


class RegistrationApiView(GenericAPIView):
    """Registration endpoint."""
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'detail': _(
                'You have signed up successfully...Verification code sent for you.' # noqa
            )},
            status=status.HTTP_200_OK
        )


class VerificationApiView(GenericAPIView):
    """Verification endpoint via SMS."""
    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user', None)
        user.is_verified = True
        user.save()
        return Response(
            {'detail': _('Your account verified successfully.')},
            status=status.HTTP_200_OK
        )


class LoginApiView(TokenObtainPairView):
    """Login endpoint with returning JWT tokens."""
    serializer_class = LoginSerializer
