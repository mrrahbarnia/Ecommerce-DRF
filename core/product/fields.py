"""
Custom fields.
"""
from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
    Custom field for generating ordering number for a specific field.
    """
    def __init__(self, unique_for_field, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        """Validating the custom field named OrderField."""
        return [
            *super().check(**kwargs),
            *self._check_unique_for_field(self, **kwargs)
        ]

    def _check_unique_for_field(self, **kwargs):
        """Validating unique_for_field attribute for this custom field."""
        if self.unique_for_field is None:
            """Returning error if 'unique_for_field' is none."""
            return [
                checks.ERROR(
                    "'unique_for_field' attribute must be set in OrderField."
                )
            ]
        elif self.unique_for_field not in [
            field.name for field in self.model._meta.get_fields()
        ]:
            """
            Returning error if the value of
            'unique_for_field' not in the model fields.
            """
            return [
                checks.ERROR(
                    """
                    Value of the 'unique_for field'
                    doesn't match to any field name.
                    """
                )
            ]
        else:
            return []

    def pre_save(self, model_instance, add):
        """Generating the order field automatically according
        to whether there is any instances in database or not."""
        if getattr(model_instance, self.attname) is None:
            queryset = self.model.objects.all()
            try:
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                queryset = queryset.filter(**query)
                last_obj = queryset.latest(self.attname)
                value = last_obj.order + 1

            except ObjectDoesNotExist:
                value = 1

            return value
        else:
            return super().pre_save(model_instance, add)
