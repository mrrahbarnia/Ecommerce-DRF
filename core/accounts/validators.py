"""
Validators for Accounts app.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_validation(phone_number):
    if len(phone_number) != 11:
        raise ValidationError(
            _(f'{phone_number} is not a valid phone number...the phone number must be exact 11 digits.') # noqa
        )
