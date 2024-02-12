"""
Admin panel for Ticketing app.
"""
from django.contrib import admin

from .models import (
    Ticketing,
    Response
)


class ResponseInline(admin.TabularInline):
    """
    Inline admin panel for using in TicketingAdmin.
    """
    model = Response


@admin.register(Ticketing)
class TicketingAdmin(admin.ModelAdmin):
    """Admin panel config for Ticketing app."""
    inlines = [ResponseInline]
