# Generated by Django 4.0 on 2022-04-25 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0032_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discounted_price',
            field=models.FloatField(default=0, max_length=255),
        ),
    ]