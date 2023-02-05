# Generated by Django 4.0 on 2023-02-01 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_subscription_is_active'),
        ('cart', '0033_deliveryaddress_shipping_class_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.customerprofile'),
        ),
    ]