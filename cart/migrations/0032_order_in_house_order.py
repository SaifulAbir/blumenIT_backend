# Generated by Django 4.0 on 2023-01-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0031_order_is_active_orderitem_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='in_house_order',
            field=models.BooleanField(default=False),
        ),
    ]
