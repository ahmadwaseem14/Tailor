# Generated by Django 5.0.7 on 2024-11-08 16:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stitching', '0015_expensetype_alter_booking_button_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='date_subscribed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
