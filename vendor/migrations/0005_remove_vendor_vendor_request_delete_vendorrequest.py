# Generated by Django 4.0 on 2023-01-04 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_delete_vendorreview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_request',
        ),
        migrations.DeleteModel(
            name='VendorRequest',
        ),
    ]
