"""
Ticketing managers.
"""
from django.db.models import (
    QuerySet,
    Manager
)
from django.utils import timezone

from django.core.cache import cache

class CustomQuerySet(QuerySet):
    """Overriding update method for cleaning cached data."""
    def update(self, **kwargs):
        cache.delete('ticket_objects')
        super(CustomQuerySet, self).update(
            updated=timezone.now(), **kwargs
        )


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)