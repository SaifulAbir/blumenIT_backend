# Generated by Django 4.0 on 2022-02-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0024_alter_order_ordered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]