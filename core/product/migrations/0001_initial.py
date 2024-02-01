# Generated by Django 4.2 on 2024-02-01 10:05

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import product.fields
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(verbose_name='attribute name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(verbose_name='value')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_value', to='product.attribute')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, verbose_name='brand name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name')),
                ('discount', models.IntegerField(default=0, verbose_name='brand discount')),
                ('description', models.TextField(blank=True, null=True, verbose_name='brand description')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, verbose_name='category name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name')),
                ('discount', models.IntegerField(default=0, verbose_name='category discount')),
                ('description', models.TextField(blank=True, null=True, verbose_name='category description')),
                ('is_active', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(verbose_name='product name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('sku', models.CharField(default=product.models.sku_generator, max_length=16, unique=True, verbose_name='sku')),
                ('stock', models.IntegerField(default=0, verbose_name='stock quantity')),
                ('price', models.DecimalField(decimal_places=4, max_digits=19, verbose_name='price')),
                ('discount', models.IntegerField(default=0, verbose_name='discount')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(verbose_name='product name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('discount', models.IntegerField(default=0, verbose_name='discount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductTypeAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_attribute_product_type', to='product.attribute')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_product_type_attribute', to='product.producttype')),
            ],
            options={
                'unique_together': {('product_type', 'attribute')},
            },
        ),
        migrations.AddField(
            model_name='producttype',
            name='attribute',
            field=models.ManyToManyField(related_name='product_type_attribute', through='product.ProductTypeAttribute', to='product.attribute'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.ImageField(upload_to=product.models.product_img_file_path, verbose_name='product image')),
                ('alt_text', models.CharField(blank=True, null=True, verbose_name='alternative text')),
                ('order', product.fields.OrderField(blank=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attr_value_product_attribute_value', to='product.attributevalue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_product_attribute_value', to='product.product')),
            ],
            options={
                'unique_together': {('product', 'attribute_value')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='attribute_value',
            field=models.ManyToManyField(related_name='product_attribute_value', through='product.ProductAttributeValue', to='product.attributevalue'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand', to='product.brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='product.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='product.producttype'),
        ),
    ]
