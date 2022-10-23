# Generated by Django 4.0 on 2022-10-20 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0108_productvariation_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('initial_quantity', models.IntegerField(default=0)),
                ('current_quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory_product', to='product.product')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
                'db_table': 'inventory',
            },
        ),
        migrations.AddField(
            model_name='productvariation',
            name='attribute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Product_variation_product_attribute', to='product.productattributes'),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Product_variation_product', to='product.product'),
        ),
        migrations.CreateModel(
            name='InventoryVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('variation_initial_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('variation_current_quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory_variation_inventory', to='product.inventory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory_variation_product', to='product.product')),
            ],
            options={
                'verbose_name': 'InventoryVariation',
                'verbose_name_plural': 'InventoryVariations',
                'db_table': 'inventory_variation',
            },
        ),
    ]