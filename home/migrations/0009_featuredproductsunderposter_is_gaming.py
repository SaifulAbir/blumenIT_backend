# Generated by Django 4.0 on 2023-01-08 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_popularproductsunderposter_is_gaming'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredproductsunderposter',
            name='is_gaming',
            field=models.BooleanField(default=False),
        ),
    ]
