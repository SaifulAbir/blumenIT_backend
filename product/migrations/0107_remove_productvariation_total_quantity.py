# Generated by Django 4.0 on 2022-10-20 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0106_remove_productvariation_product_attribute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariation',
            name='total_quantity',
        ),
    ]