# Generated by Django 4.0 on 2023-02-21 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0070_remove_subcategory_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]