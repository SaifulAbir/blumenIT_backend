# Generated by Django 4.0 on 2023-01-10 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0038_remove_savepcitems_category_savepcitems_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepc',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]