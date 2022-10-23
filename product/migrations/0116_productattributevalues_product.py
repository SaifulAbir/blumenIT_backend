# Generated by Django 4.0 on 2022-10-23 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0115_flashdealinfo_is_active_flashdealproduct_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattributevalues',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_attributes_values_product', to='product.product'),
        ),
    ]