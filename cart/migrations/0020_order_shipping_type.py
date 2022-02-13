# Generated by Django 4.0 on 2022-02-13 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0019_shippingtype_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.shippingtype'),
        ),
    ]
