# Generated by Django 4.0 on 2022-02-17 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0026_alter_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_status',
            field=models.BooleanField(default=False),
        ),
    ]