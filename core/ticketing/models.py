"""
Ticketing models.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django_lifecycle import (
    LifecycleModel,
    hook,
    AFTER_DELETE,
    AFTER_SAVE
)

from core.timestamp import TimeStamp
from .managers import CustomManager

User = get_user_model()


class Ticketing(LifecycleModel, TimeStamp):
    """
    This model belongs to Ticketing
    messages received from the customers.
    """
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ticketing'
    )
    subject = models.CharField(_('subject'), max_length=250, db_index=True)
    content = models.TextField(_('content'))
    has_response = models.BooleanField(default=False)

    objects = CustomManager()

    @hook(AFTER_DELETE)
    @hook(AFTER_SAVE)
    def invalid_cache(self):
        """
        Invalidating cache key automatically after
        any changes in the Ticketing model ocurred.
        """
        cache.delete('ticket_objects')

    def __str__(self):
        return f'{self.customer.phone_number} => {self.subject}'


class Response(TimeStamp):
    """
    This model is about messages
    that belong to supporters.
    """
    ticket = models.OneToOneField(
        Ticketing, primary_key=True,
        on_delete=models.CASCADE, related_name='tickets'
    )
    supporter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='responses'
    )
    response = models.TextField(_('response'))

    def __str__(self):
        return f'{self.supporter} => Ticket: {self.ticket.id}'
