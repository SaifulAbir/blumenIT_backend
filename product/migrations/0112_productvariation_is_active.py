# Generated by Django 4.0 on 2022-10-23 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0111_productvideoprovider_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]