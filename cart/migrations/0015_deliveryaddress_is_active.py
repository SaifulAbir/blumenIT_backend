# Generated by Django 4.0 on 2022-12-13 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_order_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]