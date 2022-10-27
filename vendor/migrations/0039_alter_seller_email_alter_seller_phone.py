# Generated by Django 4.0 on 2022-10-26 22:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0038_alter_seller_email_alter_seller_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=50, unique=True, validators=[django.core.validators.EmailValidator(message='Invalid Email')]),
        ),
        migrations.AlterField(
            model_name='seller',
            name='phone',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid phone number', regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\\s\\./0-9]*$')]),
        ),
    ]
