# Generated by Django 4.0 on 2023-02-05 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0041_tax_value_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coupon_discount_amount',
            field=models.FloatField(blank=True, default=0.0, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_cost',
            field=models.FloatField(blank=True, default=0.0, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax_amount',
            field=models.FloatField(blank=True, default=0.0, max_length=255, null=True),
        ),
    ]