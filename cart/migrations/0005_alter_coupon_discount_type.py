# Generated by Django 4.0 on 2022-11-29 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_productfilterattributes'),
        ('cart', '0004_orderitem_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_type_coupon', to='product.discounttypes'),
        ),
    ]
