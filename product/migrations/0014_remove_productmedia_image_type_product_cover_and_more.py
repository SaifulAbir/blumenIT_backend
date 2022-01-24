# Generated by Django 4.0 on 2022-01-17 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_remove_product_thumbnail_productmedia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmedia',
            name='image_type',
        ),
        migrations.AddField(
            model_name='product',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to='products'),
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='products'),
        ),
    ]