# Generated by Django 4.0 on 2023-01-04 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_delete_inventoryvariation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductColor',
        ),
    ]