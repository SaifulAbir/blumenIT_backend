# Generated by Django 4.0 on 2022-11-28 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_orderitem_attribute_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total_price',
        ),
    ]
