# Generated by Django 4.0 on 2022-10-25 07:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0031_alter_seller_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='phone',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
