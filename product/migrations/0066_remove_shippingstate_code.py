# Generated by Django 4.0 on 2023-01-29 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0065_alter_shippingclass_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingstate',
            name='code',
        ),
    ]