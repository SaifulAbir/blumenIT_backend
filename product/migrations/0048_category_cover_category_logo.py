# Generated by Django 4.0 on 2022-06-27 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0047_attributes_brand_category_discounttypes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='product_category'),
        ),
        migrations.AddField(
            model_name='category',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='product_category'),
        ),
    ]
