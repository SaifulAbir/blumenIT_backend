# Generated by Django 4.0 on 2022-02-16 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0021_order_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]