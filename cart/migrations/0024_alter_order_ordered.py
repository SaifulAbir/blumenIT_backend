# Generated by Django 4.0 on 2022-02-16 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0023_alter_order_ordered_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=True),
        ),
    ]
