"""
Accounts Models.
"""
import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from django.utils.translation import gettext_lazy as _

from core.timestamp import TimeStamp
from .managers import CustomUserManager
from .validators import phone_validation


def referral_code_generator():
    """
    Generating 10 digits code.
    """
    x = uuid.uuid4()
    return str(x).split('-')[0]


class User(
    AbstractBaseUser,
    PermissionsMixin,
    TimeStamp
):
    """
    This class defines attributes for CustomUser model.
    """
    phone_number = models.CharField(
        _('mobile number'),
        max_length=None,
        validators=[phone_validation],
        unique=True
    )
    referral_code = models.CharField(
        _('referral code'),
        max_length=100,
        default=referral_code_generator
    )
    referral_counter = models.IntegerField(
        _('referral counter'),
        default=0
    )
    default_discount = models.IntegerField(
        _('default discount'),
        default=5
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
