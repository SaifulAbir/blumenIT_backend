# Generated by Django 4.0 on 2022-09-27 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0048_remove_orderitemcombination_product_attribute_color_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitemcombination',
            name='variant_quantity',
        ),
    ]
