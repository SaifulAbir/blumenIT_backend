# Generated by Django 4.0 on 2023-02-20 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0068_alter_shippingclass_shipping_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
