# Generated by Django 4.0 on 2023-01-08 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_delete_productattributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_gaming',
            field=models.BooleanField(default=False),
        ),
    ]