# Generated by Django 4.0 on 2022-09-25 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0042_remove_order_ref_code_vendororder_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendororder',
            name='being_delivered',
        ),
    ]