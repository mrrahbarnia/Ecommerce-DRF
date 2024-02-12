"""
Custom command for creating fake products with Faker module.
"""
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from faker import Faker

from ...models import (
    Product,
    ProductImage,
    Brand,
    ProductType,
    Attribute,
    AttributeValue
)

User = get_user_model()


class Command(BaseCommand):
    """
    Custom command for creating some
    fake data to using in the Front-End.
    """
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):

        for _ in range(50):
            try:
                user = User.objects.create_superuser(
                    phone_number=self.fake.pyint(
                        min_value=11111111111, max_value=99999999999
                    ),
                    password='M13431344'
                )
                brand_name = self.fake.first_name()
                brand_obj = Brand.objects.create(
                    owner=user,
                    name=brand_name
                )

                product_type_name = self.fake.first_name()
                product_type_obj = ProductType.objects.create(
                    owner=user,
                    name=product_type_name
                )

                attribute_one = Attribute.objects.create(
                    name=self.fake.first_name()
                )
                attr_value_one = AttributeValue.objects.create(
                    attribute=attribute_one,
                    value=self.fake.color_name()
                )

                attribute_two = Attribute.objects.create(
                    name=self.fake.first_name()
                )
                attr_value_two = AttributeValue.objects.create(
                    attribute=attribute_two,
                    value=self.fake.color_name()
                )

                sample_product = Product.objects.create(
                    owner=user,
                    name=self.fake.first_name(),
                    stock=self.fake.pyint(min_value=1, max_value=300),
                    price=self.fake.pydecimal(
                        left_digits=6,
                        right_digits=3,
                        positive=True
                    ),
                    brand=brand_obj,
                    product_type=product_type_obj,
                )

                sample_product.attribute_value.add(
                    attr_value_one, attr_value_two
                )

                ProductImage.objects.create(
                    product=sample_product,
                    url=self.fake.image_url()
                )
                ProductImage.objects.create(
                    product=sample_product,
                    url=self.fake.image_url()
                )
            except IntegrityError:
                self.stdout.write(
                    'Duplicate values implemented in \
                        subcommand fake_products...'
                )
