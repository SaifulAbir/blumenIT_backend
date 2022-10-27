# Generated by Django 4.0 on 2022-10-27 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0133_remove_productvariation_product_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('variation_initial_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('variation_current_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inventory_variation_inventory', to='product.inventory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory_variation_product', to='product.product')),
                ('product_variation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inventory_variation_product_variation', to='product.productvariation')),
            ],
            options={
                'verbose_name': 'InventoryVariation',
                'verbose_name_plural': 'InventoryVariations',
                'db_table': 'inventory_variation',
            },
        ),
        migrations.DeleteModel(
            name='InventoryVariationManage',
        ),
    ]
