# Generated by Django 4.0 on 2022-10-30 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0138_remove_flashdealproduct_flashdealinfo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discounttypes',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]
