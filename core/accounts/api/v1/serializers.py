"""
Serializers for Accounts app.
"""
import uuid
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

from ...models import (
    Profile,
    Address
)

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
                    'The expiry time of the OTP(one time password) has been reached...Get a new one.' # noqa
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


class ResendVerificationSerializer(serializers.Serializer):
    """Serializer for resend verification endpoint."""
    phone_number = serializers.CharField(required=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', None)
        try:
            user = User.objects.get(phone_number=phone_number)
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': _('There is no user with this phone number.')}
            )

        # TODO: Sending OTP with provided phone_number here

        return super(ResendVerificationSerializer, self).validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password for authenticated users."""
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password1 = serializers.CharField()

    def validate(self, attrs):
        old_password = attrs.get('old_password', None)
        new_password = attrs.get('new_password', None)
        new_password1 = attrs.get('new_password1', None)
        if new_password != new_password1:
            raise serializers.ValidationError(
                {'detail': _('New passwords must be match.')}
            )

        errors = dict()
        errors['new_password'] = []
        try:
            validate_password(new_password)
        except exceptions.ValidationError as e:
            for error in list(e.messages):
                errors['new_password'].append(_(error))
        if errors['new_password'] != []:
            raise serializers.ValidationError(errors)

        attrs['old_password'] = old_password
        attrs['new_password'] = new_password
        return super(ChangePasswordSerializer, self).validate(attrs)


class ResetPasswordSerializer(ResendVerificationSerializer):
    """Serializer for Reset password endpoint."""
    def validate(self, attrs):
        phone_number = attrs.get('phone_number', None)
        try:
            user = User.objects.get(phone_number=phone_number)
            temp_pass = self.temp_password()
            user.set_password(temp_pass)
            user.save()
            # TODO: sending new password to the provided phone_number

        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': _('There is no user with this phone number.')}
            )
        return super(ResetPasswordSerializer, self).validate(attrs)

    def temp_password(self):
        """Generate and return string for temporary password."""
        temp_pass = uuid.uuid4()
        return str(temp_pass).split('-')[0]


class ProfileSerializer(serializers.ModelSerializer):
    """Profile objects serializer."""
    phone_number = serializers.CharField(
        source='user.phone_number', read_only=True
    )
    # Showing referral code to users for using in front-end
    referral_code = serializers.CharField(
        source='user.referral_code', read_only=True
    )

    class Meta:
        model = Profile
        fields = [
            'phone_number', 'email', 'first_name',
            'last_name', 'age', 'image', 'referral_code'
        ]


class AddressSerializer(serializers.ModelSerializer):
    """Address objects serializer."""
    phone_number = serializers.CharField(
        source='user.phone_number', read_only=True
    )
    address_snippet = serializers.CharField(
        source='entire_address_snippet', read_only=True
    )

    class Meta:
        model = Address
        fields = [
            'phone_number', 'province', 'city', 'street', 'alley',
            'floor', 'house_number', 'zip_code', 'telephone_number',
            'entire_address', 'address_snippet'
        ]
