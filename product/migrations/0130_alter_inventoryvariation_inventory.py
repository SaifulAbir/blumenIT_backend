# Generated by Django 4.0 on 2022-10-27 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0129_alter_inventory_current_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryvariation',
            name='inventory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inventory_variation_inventory', to='product.inventory'),
        ),
    ]
