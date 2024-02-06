"""
Custom filters for product app.
"""
from django_filters import rest_framework as filters

from ...models import Product


class ProductFilter(filters.FilterSet):
    """
    Custom filter for Product model.
    """
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    brand = filters.CharFilter(
        field_name='brand__slug', lookup_expr='icontains'
    )
    product_type = filters.CharFilter(
        field_name='product_type__slug', lookup_expr='icontains'
    )

    class Meta:
        model = Product
        fields = ['brand', 'product_type']
