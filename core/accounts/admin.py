"""
Admin for the Accounts model.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    User,
    Profile,
    Address
)


class ProfileAdminInline(admin.StackedInline):
    """Profile model inline for using in CustomUser model admin site."""
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        """
        Thumbnail of the profile picture in the admin site.
        """
        if instance.image != '':
            return format_html(
                f'<img src="{instance.image.url}" class="thumbnail" />'
            )
        return ''

    class Media:
        """Importing css styles into admin site for profile picture."""
        css = {
            'all': ['styles/styles.css']
        }


class AddressAdminInline(admin.StackedInline):
    """Address model inline for using in CustomUser model admin site."""
    model = Address
    can_delete = False
    verbose_name_plural = _('Address')
    fk_name = 'user'


@admin.register(User)
class UserAdmin(UserAdmin):
    """For customizing admin page."""
    inlines = (ProfileAdminInline, AddressAdminInline)
    ordering = ['id']
    model = User
    list_display = ("phone_number",)
    fieldsets = (
        (None, {'fields': (
            "phone_number", "referral_counter", "default_discount", "password"
        )}),
        (_("Permissions"),
            {'fields':
             ("is_active", "is_verified", "is_superuser",
              "is_staff", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ("last_login",)
    add_fieldsets = (
        (None, {
            "fields": (
                "phone_number",
                "password1",
                "password2",
                "is_active",
                "is_verified",
                "is_staff",
                "is_superuser",
            )
        }),
    )
