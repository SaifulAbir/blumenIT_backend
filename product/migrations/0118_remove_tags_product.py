# Generated by Django 4.0 on 2022-10-26 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0117_specificationvalue_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='product',
        ),
    ]
