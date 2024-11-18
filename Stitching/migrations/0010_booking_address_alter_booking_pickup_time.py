# Generated by Django 5.0.7 on 2024-08-07 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stitching', '0009_city_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='address',
            field=models.CharField(default='hi', max_length=255),
        ),
        migrations.AlterField(
            model_name='booking',
            name='pickup_time',
            field=models.CharField(max_length=50),
        ),
    ]
