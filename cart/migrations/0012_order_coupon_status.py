# Generated by Django 4.0 on 2022-11-30 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_status',
            field=models.BooleanField(default=False),
        ),
    ]
