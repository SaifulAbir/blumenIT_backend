# Generated by Django 4.0 on 2022-09-27 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0095_producttags_tag'),
        ('cart', '0046_orderitemcombination'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitemcombination',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitemcombination',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item_combination_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='orderitemcombination',
            name='variant_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
