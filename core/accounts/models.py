"""
Accounts Models.
"""
import os
import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from core.timestamp import TimeStamp
from .managers import (
    CustomUserManager
)
from .validators import (
    phone_validator,
    profile_image_size_validator,
    age_validator
)


def referral_code_generator():
    """
    Generating 10 digits code.
    """
    x = uuid.uuid4()
    return str(x).split('-')[0]


def profile_img_file_path(instance, filename):
    """
    Generating unique path for every profile images.
    """
    ext = os.path.splitext(filename)[1]
    file_name = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'profile', file_name)


class User(
    AbstractBaseUser,
    PermissionsMixin
):
    """
    This class defines attributes of the CustomUser model.
    """
    phone_number = models.CharField(
        _('mobile number'),
        max_length=None,
        validators=[phone_validator],
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
        default=0
    )
    used_referral_code = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # verification via SMS

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Profile(TimeStamp):
    """
    This class defines attributes of the Profile model.
    """
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile'
    )
    email = models.EmailField(
        _('email address'),
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _('first name'),
        max_length=100,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=100,
        null=True,
        blank=True
    )
    age = models.IntegerField(
        null=True, blank=True,
        validators=[age_validator]
    )
    image = models.ImageField(
        _('profile image'),
        upload_to=profile_img_file_path,
        validators=[profile_image_size_validator],
        null=True,
        blank=True
    )

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.user.phone_number


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Signal for adding profile object for the user
    instance automatically after creating user object.
    """
    if created:
        Profile.objects.create(user=instance)


class Address(TimeStamp):
    """
    This class defines attributes of the Address model.
    """
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='address',
    )
    province = models.CharField(
        _('province'),
        max_length=150,
        null=True,
        blank=True
    )
    city = models.CharField(
        _('city'),
        max_length=150,
        null=True,
        blank=True
    )
    street = models.CharField(
        _('street'),
        max_length=150,
        null=True,
        blank=True
    )
    alley = models.CharField(
        _('alley'),
        max_length=150,
        null=True,
        blank=True
    )
    floor = models.CharField(
        _('floor'),
        max_length=150,
        null=True,
        blank=True
    )
    house_number = models.CharField(
        _('house number'),
        max_length=150,
        null=True,
        blank=True
    )
    zip_code = models.CharField(
        _('zip code'),
        max_length=150,
        null=True,
        blank=True
    )
    telephone_number = models.CharField(
        _('telephone number'),
        max_length=150,
        null=True,
        blank=True
    )
    entire_address = models.TextField(
        _('entire address'),
        null=True,
        blank=True
    )

    def entire_address_snippet(self):
        """
        Truncating the entire address field.
        """
        truncated_address = Truncator(self.entire_address).words(6)
        return truncated_address

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = 'Addresses'


@receiver(post_save, sender=User)
def address(sender, instance, created, **kwargs):
    """
    Signal for adding address object for the user
    instance automatically after creating user object.
    """
    if created:
        Address.objects.create(user=instance)
