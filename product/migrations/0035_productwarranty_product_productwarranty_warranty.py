# Generated by Django 4.0 on 2023-01-08 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0034_remove_productwarranty_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productwarranty',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_warranty_product', to='product.product'),
        ),
        migrations.AddField(
            model_name='productwarranty',
            name='warranty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_warranty_warranty', to='product.warranty'),
        ),
    ]
