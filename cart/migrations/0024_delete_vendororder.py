# Generated by Django 4.0 on 2023-01-04 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0023_alter_wishlist_options_alter_wishlist_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VendorOrder',
        ),
    ]
