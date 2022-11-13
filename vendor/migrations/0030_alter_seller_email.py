# Generated by Django 4.0 on 2022-10-25 05:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0029_alter_seller_email_alter_seller_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=50, unique=True, validators=[django.core.validators.EmailValidator(message='Invalid Email')]),
        ),
    ]