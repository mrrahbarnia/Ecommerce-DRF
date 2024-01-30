"""
Managers and custom query set for product app.
"""
from django.db import models


class Active(models.QuerySet):
    """Queryset for filtering verified
    users in Profile and Address models."""

    def active(self):
        queryset = self.filter(is_active=True)
        return queryset
