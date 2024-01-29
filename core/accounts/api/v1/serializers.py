"""
Serializers for Accounts app.
"""
import random
from datetime import (
    datetime,
    timedelta
)

from django.utils import timezone
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from ..models import (
#     Profile,
#     Address
# )

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    referral = serializers.CharField(
        max_length=30, required=False,
        help_text=_('Enter your referral code if you have any.')
    )
    password1 = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'password', 'password1', 'referral'
        ]

    def validate(self, attrs):
        """
        Validating passwords and also get input referral code
        and check whether if any user exists with that or not.
        """
        referral = attrs.get('referral', None)
        password = attrs.get('password', None)
        password1 = attrs.get('password1', None)
        if referral is not None:
            try:
                user_obj = User.objects.get(referral_code=referral)
                user_obj.referral_counter += 1
                user_obj.save()
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {'referral': _('The referral code is not valid.')}
                )

        if password != password1:
            raise serializers.ValidationError(
                {'detail': _('Passwords must be match.')}
            )

        errors = dict()
        errors['password'] = []
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            for error in list(e.messages):
                errors['password'].append(_(error))
        if errors['password'] != []:
            raise serializers.ValidationError(errors)
        return super(RegistrationSerializer, self).validate(attrs)

    def create(self, validated_data):
        """Creating user objects with encrypted password."""
        otp = random.randint(100000, 999999)
        # Each SMS is valid for 3 minutes
        otp_expiry = datetime.now() + timedelta(minutes=3)

        validated_data.pop('password1')
        referral_code = validated_data.pop('referral', None)
        if referral_code:
            encrypted_user = User.objects.create_user(
                otp=otp,
                otp_expiry=otp_expiry,
                used_referral_code=True,
                **validated_data
            )
            return encrypted_user
        else:
            encrypted_user = User.objects.create_user(
                otp=otp,
                otp_expiry=otp_expiry,
                **validated_data
            )
            return encrypted_user


class VerificationSerializer(serializers.Serializer):
    """Serializer for verification with OTP."""
    otp = serializers.IntegerField()

    def validate(self, attrs):
        """Validating One time password."""
        otp = attrs.get('otp', None)

        try:
            user = User.objects.get(otp=otp)
            if user.is_verified:
                raise serializers.ValidationError(
                    {'detail': _('You have already been verified.')}
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': _('The OTP(one time password) is invalid.')}
            )

        otp_expiry = user.otp_expiry
        if otp_expiry < timezone.now():
            raise serializers.ValidationError(
                {'detail': _(
                    'The expiry time of the OTP(one time password) has been reached...Try again.' # noqa
                )}
            )
        attrs['user'] = user
        return super(VerificationSerializer, self).validate(attrs)


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for login endpoint."""

    def validate(self, attrs):
        validated_data = super(LoginSerializer, self).validate(attrs)

        validated_data['phone_number'] = self.user.phone_number
        # Showing referral code to users for using in front-end
        validated_data['referral_code'] = self.user.referral_code

        return validated_data
