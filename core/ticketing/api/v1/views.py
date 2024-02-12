"""
Endpoints of the Ticketing app.
"""
from django.db.models import Q
from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import (
    viewsets,
    status
)

from .serializers import (
    TicketingSerializer
)

from ...models import (
    Ticketing
)


class TicketApiViewSet(viewsets.ModelViewSet):
    """Endpoints for ticketing."""
    serializer_class = TicketingSerializer

    def get_queryset(self):
        queryset = cache.get('ticket_objects')
        if queryset is None:
            queryset = Ticketing.objects.select_related(
                'customer'
            ).all()
            cache.set('ticket_objects', queryset)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @action(
            methods=['GET'],
            detail=False,
            url_path=r'search/(?P<subject_or_content>[\w-]+)'
    )
    def search_by_subject_or_content(
        self, request, subject_or_content=None, *args, **kwargs
    ):
        """
        Search tickets by 'subject_or_content' word either
        if content or subject insensitivity contain it.
        """
        queryset = self.get_queryset().filter(
            Q(subject__icontains=subject_or_content) | Q(content__icontains=subject_or_content)
        )
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
            methods=['GET'],
            detail=False,
            url_path=r'phone-number/(?P<phone_number>[\w-]+)'
    )
    def list_all_tickets_belong_to_specific_user(
        self, request, phone_number=None, *args, **kwargs
    ):
        """
        List all tickets which belong to a provided phone number.
        """
        queryset = self.get_queryset().filter(
            customer__phone_number=phone_number
        )
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'without-response'
    )
    def list_all_tickets_without_response(
        self, request, *args, **kwargs
    ):
        """
        List all tickets which has no responses.
        """
        queryset = self.get_queryset().filter(has_response=False)
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
