"""
Validators for Accounts app.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_validator(phone_number):
    """Validating phone number."""
    if len(phone_number) != 11:
        raise ValidationError(
            _(f'{phone_number} is not a valid phone number...the phone number must be exact 11 digits.') # noqa
        )


def profile_image_size_validator(file):
    """Validating profile image size to be less than 5MB."""
    max_size_mb = settings.MAX_PROFILE_IMAG_SIZE_MB

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(_(f'Max file size is {max_size_mb}MB'))


def age_validator(age):
    """
    Validating age.
    """
    if age > 99:
        raise ValidationError(_(
            f'Age must be less than 99 years old...{age} is not valid.'
        ))
    elif age < 1:
        raise ValidationError(_(
            f'Age must be greater than 1 year old...{age} is not valid.'
        ))
