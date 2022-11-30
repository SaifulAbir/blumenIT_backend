# Generated by Django 4.0 on 2022-11-29 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_coupon_discount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='amount',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='min_shopping',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
