# Generated by Django 4.0 on 2022-11-27 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_product_warranty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='category',
            name='logo',
        ),
    ]
