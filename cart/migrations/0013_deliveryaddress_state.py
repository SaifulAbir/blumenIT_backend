# Generated by Django 4.0 on 2022-11-30 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_order_coupon_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='state',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
