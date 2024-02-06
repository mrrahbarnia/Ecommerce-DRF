"""
Admin panel for product app.
"""
from django.contrib import admin

from .models import (
    Product,
    Brand,
    ProductType,
    ProductImage,
    Attribute,
    AttributeValue,
    ProductTypeAttribute,
    ProductAttributeValue
)


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    model = ProductAttributeValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        # ProductAttributeValueInline,
        ProductImageAdmin
    ]


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]


admin.site.register(Brand)

# admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductType)
# admin.site.register(ProductImage)
admin.site.register(ProductTypeAttribute)
# admin.site.register(ProductAttributeValue)
