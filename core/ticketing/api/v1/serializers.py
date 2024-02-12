"""
Serializers for the Ticketing app.
"""
from rest_framework import serializers
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

from ...models import (
    Ticketing,
    Response
)


class TicketingSerializer(serializers.ModelSerializer):
    """Serializing Tickets."""
    customer = serializers.CharField(
        source='customer.phone_number', read_only=True
    )
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Ticketing
        fields = ['customer', 'subject', 'content', 'absolute_url']

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            reverse('ticketing-detail', args=[obj.pk])
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)
        if request.parser_context.get('kwargs').get('pk'):
            data.pop('absolute_url')
        return data
