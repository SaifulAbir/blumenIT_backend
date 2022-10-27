# Generated by Django 4.0 on 2022-10-27 00:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0040_alter_seller_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(default='', max_length=50, validators=[django.core.validators.EmailValidator(message='Invalid Email')]),
        ),
        migrations.AlterField(
            model_name='seller',
            name='name',
            field=models.CharField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='seller',
            name='phone',
            field=models.CharField(default='', max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\\s\\./0-9]*$')]),
        ),
    ]
