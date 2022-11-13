# Generated by Django 4.0 on 2022-10-23 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0057_discounttype_coupon_discount_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_type', to='cart.discounttype'),
        ),
        migrations.AlterModelTable(
            name='discounttype',
            table='discount_type',
        ),
    ]