# Generated by Django 4.0 on 2022-07-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0068_remove_productcombinations_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcombinations',
            name='product_attribute_color_code',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='productcombinations',
            name='product_attribute_value',
            field=models.CharField(default='', max_length=500),
        ),
    ]