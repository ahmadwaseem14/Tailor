# Generated by Django 5.0.7 on 2024-08-05 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stitching', '0007_alter_button_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fabric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('specifications', models.JSONField(blank=True, default=dict, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sku', models.CharField(editable=False, max_length=4, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('video', models.FileField(blank=True, null=True, upload_to='products/')),
                ('in_stock', models.BooleanField(default=True)),
            ],
        ),
    ]