# Generated by Django 4.0 on 2022-02-16 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0022_remove_order_start_date_alter_order_ordered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(),
        ),
    ]
