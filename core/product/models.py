"""
Product models.
"""
import os
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import Truncator
from django_lifecycle import (
    LifecycleModel,
    hook,
    AFTER_DELETE,
    AFTER_SAVE
)

from autoslug import AutoSlugField

from .fields import OrderField
from .managers import (
    Active,
    CustomManager
)
from core.timestamp import TimeStamp

User = get_user_model()


def product_img_file_path(instance, filename):
    """
    Generating unique path for every product images.
    """
    ext = os.path.splitext(filename)[1]
    file_name = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'product', file_name)


def sku_generator():
    """Generating unique sku for products."""
    x = uuid.uuid4()
    y = str(x.int)[:15]
    return y


class Brand(TimeStamp):
    """
    This class defines attributes of the Brand model.
    """
    name = models.CharField(
        _('brand name'),
        max_length=None,
        unique=True
    )
    slug = AutoSlugField(
        populate_from='name',
        db_index=True,
        editable=False,
        always_update=True
    )
    discount = models.PositiveIntegerField(_('brand discount'), default=0)
    description = models.TextField(
        _('brand description'),
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    objects = Active.as_manager()

    def desc_snippet(self):
        """Return snippet for description fields."""
        truncated_desc = Truncator(self.description).words(12)
        return truncated_desc

    def __str__(self):
        return self.name


class ProductImage(TimeStamp):
    """
    This class defines attributes of the ProductImage model.
    """
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images'
    )
    url = models.ImageField(
        _('product image'),
        upload_to=product_img_file_path
    )
    alt_text = models.CharField(
        _('alternative text'),
        max_length=None,
        null=True,
        blank=True,
    )
    order = OrderField(unique_for_field='product', blank=True)

    def clean(self, exclude=None):
        """Validating multiple fields with clean_fields
        method for preventing from inserting duplicate values."""
        queryset = ProductImage.objects.filter(product=self.product)

        for object in queryset:
            if self.id != object.id and self.order == object.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        """Save method for running clean method."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"'{self.product.name}'=> PATH: {self.url}"


class Attribute(TimeStamp):
    """
    This class defines attributes of the Attribute model.
    """
    name = models.CharField(
        _('attribute name'), max_length=None
    )

    def __str__(self):
        return self.name


class AttributeValue(TimeStamp):
    """
    This class defines attributes of the AttributeValue model.
    """
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name='attribute_value'
    )
    value = models.CharField(_('value'), max_length=None)

    def __str__(self):
        return f'{self.attribute.name}: {self.value}'


class Product(LifecycleModel, TimeStamp):
    """
    This class defines attributes of the Product model.
    """
    name = models.CharField(_('product name'), max_length=None)
    slug = AutoSlugField(
        populate_from='name',
        db_index=True,
        editable=False,
        always_update=True
    )
    description = models.TextField(_('description'), null=True, blank=True)
    sku = models.CharField(
        _('sku'),
        max_length=16,
        unique=True,
        default=sku_generator
    )
    stock = models.IntegerField(_('stock quantity'), default=0)
    price = models.DecimalField(_('price'), max_digits=20, decimal_places=3)
    discount = models.PositiveIntegerField(_('discount'), default=0)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='brand'
    )
    product_type = models.ForeignKey(
        'ProductType',
        on_delete=models.PROTECT,
        related_name='product'
    )
    is_active = models.BooleanField(default=True)
    attribute_value = models.ManyToManyField(
        AttributeValue,
        related_name='product_attribute_value',
        through='ProductAttributeValue'
    )

    objects = CustomManager()
    # objects = Active.as_manager()
    

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def invalid_cache(self):
        """
        Invalidating cache key automatically after any changes in the product model.
        """
        cache.delete('product_objects')

    def desc_snippet(self):
        """Return snippet for description fields."""
        truncated_desc = Truncator(self.description).words(12)
        return truncated_desc

    def __str__(self):
        return self.name


class ProductType(TimeStamp):
    """
    This class defines attributes of the ProductType model.
    """
    name = models.CharField(
        _('product type name'),
        max_length=None,
        unique=True
    )
    slug = AutoSlugField(
        populate_from='name',
        db_index=True,
        editable=False,
        always_update=True
    )
    discount = models.PositiveIntegerField(_('discount'), default=0)
    attribute = models.ManyToManyField(
        Attribute,
        related_name='product_type_attribute',
        through='ProductTypeAttribute'
    )
    is_active = models.BooleanField(default=True)

    objects = Active.as_manager()

    def __str__(self):
        return self.name


class ProductAttributeValue(TimeStamp):
    """
    Link table for many to many relations
    between Product and AttributeValue models.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_product_attribute_value'
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name='attr_value_product_attribute_value'
    )

    def clean(self):
        """
        Preventing from entering two same
        attributes to a specific product.
        """
        qs = ProductAttributeValue.objects.filter(product=self.product).filter(
            attribute_value=self.attribute_value
        ).exists()

        if not qs:
            attributes = Attribute.objects.filter(
                attribute_value__product_attribute_value=self.product
            ).values_list('name', flat=True)
            if self.attribute_value.attribute.name in list(attributes):
                raise ValidationError(_('Duplicate attribute exists.'))

    def save(self, *args, **kwargs):
        """Ensure executing clean function."""
        self.full_clean()
        return super().save()

    def __str__(self):
        return f'{self.product} => \
            {self.attribute_value.attribute.name}: \
                {self.attribute_value.value}'

    class Meta:
        unique_together = ('product', 'attribute_value')


class ProductTypeAttribute(TimeStamp):
    """
    Link table for many to many relations
    between ProductType and Attribute models.
    """
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='link_product_type_attribute'
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name='link_attribute_product_type'
    )

    def __str__(self):
        return f'{self.product_type}=> Attribute: {self.attribute}'

    class Meta:
        unique_together = ('product_type', 'attribute')
