# Generated by Django 4.0 on 2022-10-27 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0132_alter_inventoryvariationmanage_inventory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariation',
            name='product_color',
        ),
    ]