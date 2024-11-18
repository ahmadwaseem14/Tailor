# Generated by Django 5.0.7 on 2024-08-03 15:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stitching', '0004_products_specificationtemplate_delete_button'),
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('specifications', models.JSONField(default=dict)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('sku', models.CharField(default='4893', max_length=4, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='media/videos/')),
                ('in_stock', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Products',
        ),
        migrations.DeleteModel(
            name='SpecificationTemplate',
        ),
    ]
