# Generated by Django 4.0 on 2022-10-25 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0035_alter_seller_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
