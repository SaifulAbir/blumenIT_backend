# Generated by Django 4.0 on 2023-01-24 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0052_alter_offer_offer_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='offer_category',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='product_category',
        ),
    ]
