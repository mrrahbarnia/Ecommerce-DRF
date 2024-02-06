"""
Views for Product app.
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .filters import ProductFilter
from .pagination import DefaultPagination
from .serializers import (
    BrandSerializer,
    ProductTypeSerializer,
    ProductSerializer
)
from ...models import (
    Brand,
    ProductType,
    Product
)


class BrandApiViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    pagination_class = DefaultPagination
    queryset = Brand.objects.active()
    lookup_field = 'slug'


class ProductTypeApiViewSet(viewsets.ModelViewSet):
    serializer_class = ProductTypeSerializer
    pagination_class = DefaultPagination
    queryset = ProductType.objects.active()
    lookup_field = 'slug'


class ProductApiViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter
    lookup_field = 'sku'

    def retrieve(self, request, sku=None, *args, **kwargs):
        """
        Overriding retrieve method for increasing products views.
        """
        obj = get_object_or_404(self.get_queryset(), sku=sku)
        obj.views += 1
        obj.save()
        serializer = self.serializer_class(
            obj, many=False, context={'request': request}
        )
        return Response(serializer.data)

    def get_queryset(self):
        """Returning queryset based on cached data."""
        queryset = cache.get('product_objects')
        if queryset is None:
            queryset = Product.objects.filter(
                is_active=True
            ).select_related(
                'brand'
            ).select_related(
                'product_type'
            ).prefetch_related(
                'attribute_value'
            ).prefetch_related(
                'images'
            ).prefetch_related(
                'attribute_value__attribute'
            )
            cache.set('product_objects', queryset)
        return queryset

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'brand/(?P<brand_slug>[\w-]+)'
    )
    def product_list_with_specific_brand_slug(self, request, brand_slug=None):
        """Listing products which belong to a specific brand."""
        filtered_queryset = self.get_queryset().filter(
            brand__slug__icontains=brand_slug)
        serializer = self.serializer_class(
            filtered_queryset, many=True, context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'product-type/(?P<product_type_slug>[\w-]+)'
    )
    def product_list_with_specific_product_type_slug(
        self, request, product_type_slug=None
    ):
        """Listing products which belong to a specific product type."""
        filtered_queryset = self.get_queryset().filter(
            product_type__slug__icontains=product_type_slug
        )
        serializer = self.serializer_class(
            filtered_queryset, many=True, context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'product-slug/(?P<product_slug>[\w-]+)'
    )
    def product_list_with_specific_product_slug(
        self, request, product_slug=None
    ):
        """Listing products which contains entered slug."""
        filtered_queryset = self.get_queryset().filter(
            slug__icontains=product_slug
        )
        serializer = self.serializer_class(
            filtered_queryset, many=True, context={'request': request}
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'special-products'
    )
    def special_products(self, request, *args, **kwargs):
        """Return 20 products with most views numbers."""
        queryset = self.get_queryset().order_by('-views')[:20]
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)
