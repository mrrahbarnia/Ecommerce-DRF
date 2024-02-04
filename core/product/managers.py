"""
Managers and custom query set for product app.
"""
from django.utils import timezone
from django.db import models
from django.core.cache import cache
from django.db.models import (
    QuerySet,
    Manager
)


class Active(models.QuerySet):
    """Queryset for filtering verified
    users in Profile and Address models."""

    def active(self):
        queryset = self.filter(is_active=True)
        return queryset


class CustomQuerySet(QuerySet):
    """Overriding update method for cleaning cached data."""
    def update(self, **kwargs):
        cache.delete('product_objects')
        super(CustomQuerySet, self).update(
            updated=timezone.now(), **kwargs
        )


class CustomManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)
