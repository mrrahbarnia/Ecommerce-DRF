"""
Accounts app view's.
"""
import logging

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegistrationSerializer,
    VerificationSerializer,
    LoginSerializer,
    ResendVerificationSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer
)

logger = logging.getLogger(__name__)


class RegistrationApiView(GenericAPIView):
    """Registration endpoint."""
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        phone_number = serializer.validated_data.get('phone_number', None)
        if phone_number:
            self.send_otp(phone_number=phone_number)

        return Response(
            {'detail': _(
                'You have signed up successfully...Verification code sent for you.' # noqa
            )},
            status=status.HTTP_200_OK
        )

    def send_otp(self, phone_number):
        # Sending OTP
        pass


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


class ResendVerificationApiView(GenericAPIView):
    """Resending verification code."""
    serializer_class = ResendVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {'detail': _(
                'A new OTP(one time password) generated and sent for you.'
            )}
        )


class LoginApiView(TokenObtainPairView):
    """Login endpoint with returning JWT tokens."""
    serializer_class = LoginSerializer


class ChangePasswordApiView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve the authenticated user."""
        return self.request.user

    def put(self, request, *args, **kwargs):
        user_object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get('old_password', None)
        new_password = serializer.validated_data.get('new_password', None)

        if not user_object.check_password(old_password):
            return Response(
                {'old_password': _('Wrong old password.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_object.set_password(new_password)
        user_object.save()
        return Response(
            {'detail': _('Your password changed successfully.')},
            status=status.HTTP_200_OK
        )


class ResetPasswordApiView(GenericAPIView):
    """Reset password endpoint."""
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': _('A temporary password sent for you...Please login with that and change it...')}, # noqa
            status=status.HTTP_200_OK
        )
