# Generated by Django 4.0 on 2022-12-26 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0020_alter_order_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_status',
        ),
    ]