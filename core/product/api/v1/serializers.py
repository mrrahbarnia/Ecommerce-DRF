"""
Serializers for Product app.
"""
from rest_framework import serializers

from ...models import (
    Brand,
    ProductImage,
    Attribute,
    AttributeValue,
    ProductType,
    Product,
)


class BrandSerializer(serializers.ModelSerializer):
    """Serializing the Brand model."""
    description_snippet = serializers.ReadOnlyField(source='desc_snippet')

    class Meta:
        model = Brand
        fields = [
            'name', 'discount', 'description',
            'description_snippet',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)
        if request.parser_context.get('kwargs').get('slug'):
            data.pop('description_snippet')
        else:
            data.pop('description')
        return data


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['name']


class ProductTypeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=True, required=False)

    class Meta:
        model = ProductType
        fields = ['name', 'discount','attribute']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['attribute_names']= []
        attributes = data.pop('attribute')
        for attribute in attributes:
            data['attribute_names'].append(attribute['name'])
        return data

    def _get_or_create_attributes(self, attributes, product_type_obj):
        for attribute in attributes:
            attribute_obj, created = Attribute.objects.get_or_create(
                **attribute
            )
            product_type_obj.attribute.add(attribute_obj)

    def create(self, validated_data):
        attributes = validated_data.pop('attribute', [])
        product_type_obj = ProductType.objects.create(**validated_data)
        self._get_or_create_attributes(attributes, product_type_obj)
        return product_type_obj
    
    def update(self, instance, validated_data):
        attributes = validated_data.pop('attribute', None)
        if attributes:
            instance.attribute.clear()
            self._get_or_create_attributes(attributes, instance)
        instance = super(ProductTypeSerializer, self).update(instance, validated_data)
        return instance


class ProductImageSerializer(serializers.ModelSerializer):
    # product = serializers.CharField(source='product.name')
    class Meta:
        model = ProductImage
        fields = ['order', 'url', 'alt_text']
        extra_kwargs = {'url': {'required': True}}
        read_only_fields = ['order']


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(source='attribute.name')
    class Meta:
        model = AttributeValue
        fields = ['attribute', 'value']


class ProductSerializer(serializers.ModelSerializer):

    brand = serializers.CharField(source='brand.name')
    brand_url = serializers.HyperlinkedRelatedField(
        source='brand', many=False, read_only=True,
        view_name='brand-detail', lookup_field='slug'
    )
    product_type = serializers.CharField(source='product_type.name')
    product_type_url = serializers.HyperlinkedRelatedField(
        source='product_type', many=False, read_only=True,
        view_name='product-type-detail', lookup_field='slug'
    )
    attribute_value = AttributeValueSerializer(many=True, required=False)
    images = ProductImageSerializer(many=True, required=False, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    description_snippet = serializers.ReadOnlyField(source='desc_snippet')
    absolute_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'description_snippet', 'sku',
            'stock', 'price', 'discount', 'brand', 'brand_url',
            'product_type', 'product_type_url', 'attribute_value',
            'images', 'absolute_url', 'uploaded_images'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)
        if request.parser_context.get('kwargs').get('sku'):
            pass
        else:
            data.pop('description')

        attributes_values = {}
        attr_values = data.pop('attribute_value')
        for attribute_value in attr_values:
            attributes_values.update({attribute_value['attribute']: attribute_value['value']})
        data.update({'specifications': attr_values})
        return data

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.sku)

    def _get_or_create_brand(self, brand):
        return Brand.objects.get_or_create(name=brand)

    def _get_or_create_product_type(self, product_type):
        return ProductType.objects.get_or_create(name=product_type)

    def _get_or_create_attribute_value(self, attribute_values, product_obj):
        pass

    def _get_or_create_images(self, images, product_obj):
        for image in images:
            image.pop('product', None)
            image.pop('order', None)
            ProductImage.objects.create(
                product=product_obj,
                **image
            )

    def create(self, validated_data):
        brand_name = validated_data.pop('brand', None)
        product_type_name = validated_data.pop('product_type', None)
        attribute_values = validated_data.pop('attribute_value', [])
        product_images = validated_data.pop('uploaded_images', [])

        brand_obj = self._get_or_create_brand(brand_name['name'])
        product_type_obj = self._get_or_create_product_type(
            product_type_name['name']
        )

        product_obj = Product.objects.create(
            brand=brand_obj[0], product_type=product_type_obj[0], **validated_data
        )

        # if attribute_values:
        #     self._get_or_create_attribute_value(attribute_values, product_obj)

        self._get_or_create_images(product_images, product_obj)

        return product_obj


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
