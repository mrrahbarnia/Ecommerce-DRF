"""
Documents for the ElasticSearch engine.
"""
from django.contrib.auth import get_user_model
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import (
    Document,
    fields
)

from product.models import (
    Product,
    Brand,
    ProductType
)


@registry.register_document
class ProductDocument(Document):
    # owner = fields.ObjectField(properties={
    #     'id': fields.IntegerField(),
    #     'phone_number': fields.IntegerField(),
    # })
    # brand = fields.ObjectField(properties={
    #     'id': fields.IntegerField(),
    #     'name': fields.TextField()
    # })
    # product_type = fields.ObjectField(properties={
    #     'id': fields.IntegerField(),
    #     'name': fields.TextField()
    # })
    # product

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


    class Django:
        model = Product
        fields = [
            'name',
            'description',
            'sku',
            'stock',
            'price',
            'discount',
            'views',
            'is_active',
            'created_at',
            'updated_at'
        ]
