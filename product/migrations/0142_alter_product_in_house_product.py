# Generated by Django 4.0 on 2022-11-13 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0141_product_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='in_house_product',
            field=models.BooleanField(default=False),
        ),
    ]
