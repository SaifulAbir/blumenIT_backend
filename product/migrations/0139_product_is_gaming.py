# Generated by Django 4.0 on 2022-11-06 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0138_remove_flashdealproduct_flashdealinfo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_gaming',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
